<template>
  <v-card
    elevation="1"
    width="350"
    height="250"
    class="flex-grow-1 d-flex flex-column align-start ma-1"
    :loading="loading"
  >
    <v-card-title style="width: 100%">
      <span :class="[statusColor, 'title-overflow']" :title="content.name">
        <v-icon v-if="statusIcon" class="mr-1" :color="statusBgColor">{{
          statusIcon
        }}</v-icon>
        {{ content.name }}</span
      >
    </v-card-title>
    <v-card-subtitle>
      <v-icon dense class="mr-1">mdi-link-variant</v-icon>
      <a :href="content.url" target="_blank" class="mr-1">View</a>
      <span class="mr-1">·</span>
      <v-icon dense class="mr-1">mdi-heart</v-icon>
      <span class=" mr-2">{{ content.crawl_stars }}</span>
      <span class="mr-1">·</span>
      <v-icon dense class="mr-1">mdi-directions-fork</v-icon>
      <span class=" mr-2">{{ content.crawl_forks }}</span>
      <span class="mr-1">·</span>
      <v-icon dense class="mr-1">mdi-note-text-outline</v-icon>
      <span class="">{{ content.crawl_issues }}</span>
    </v-card-subtitle>
    <v-card-text style="overflow: hidden">
      {{ content.description }}
    </v-card-text>
    <v-card-actions class="mt-auto" style="width: 100%; min-width: 100%;">
      <v-select v-model="repoStatus" :items="statusList" full-width dense />
    </v-card-actions>
  </v-card>
</template>
<script>
import {
  MapRepositoryStatus,
  SelectRepositoryStatus,
} from "../utils/enumerations.js";

export default {
  props: {
    content: Object,
  },
  data() {
    return {
      repoStatus: this.content.status,
      loading: false,
      statusList: SelectRepositoryStatus,
    };
  },
  watch: {
    repoStatus: function(val) {
      this.loading = "primary";

      fetch("/api/repos/" + this.content.id, {
        headers: {
          "Content-Type": "application/json",
        },
        method: "PATCH",
        body: JSON.stringify({ status: val }),
      }).then((response) => {
        if (response.status != 200) {
          console.log("Can not change status");
          // TODO implement a global notification center
        }
        this.loading = false;
      });
    },
  },
  computed: {
    statusBgColor: function() {
      if (MapRepositoryStatus.has(this.repoStatus))
        return MapRepositoryStatus.get(this.repoStatus)["color"];
      return null;
    },
    statusColor: function() {
      if (MapRepositoryStatus.has(this.repoStatus)) {
        let bgColor = MapRepositoryStatus.get(this.repoStatus)["color"];
        if (bgColor) {
          let sColor = bgColor.split(" ");
          sColor[0] = sColor[0] + "--text";
          return sColor.join(" ");
        }
      }
      return null;
    },
    statusIcon: function() {
      if (MapRepositoryStatus.has(this.repoStatus))
        return MapRepositoryStatus.get(this.repoStatus)["icon"];
      return null;
    },
  },
};
</script>
<style scoped>
.title-overflow {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 100%;
}
</style>
