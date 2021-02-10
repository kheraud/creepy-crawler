<template>
  <v-card
    elevation="1"
    width="350"
    height="250"
    :class="[
      statusConf['color'],
      statusConf['contrastTextColor'],
      'flex-grow-1',
      'd-flex',
      'flex-column',
      'align-start',
      'ma-1',
    ]"
    :loading="loading"
    :color="fgColor"
  >
    <v-card-title style="width: 100%" :class="statusConf['contrastTextColor']">
      <span class="title-overflow" :title="content.name">
        <v-icon
          v-if="statusConf['icon']"
          class="mr-1"
          :color="statusConf['contrastColor']"
          >{{ statusConf["icon"] }}</v-icon
        >
        {{ content.name }}</span
      >
    </v-card-title>
    <v-card-subtitle :class="statusConf['contrastTextColor']">
      <v-icon dense :class="[statusConf['contrastTextColor'], 'mr-1']"
        >mdi-link-variant</v-icon
      >
      <a
        :href="content.url"
        target="_blank"
        :class="[statusConf['contrastTextColor'], 'mr-1']"
        >View</a
      >
      <span class="mr-1">·</span>
      <v-icon dense :class="[statusConf['contrastTextColor'], 'mr-1']"
        >mdi-heart</v-icon
      >
      <span class="mr-2">{{ content.crawl_stars }}</span>
      <span class="mr-1">·</span>
      <v-icon dense :class="[statusConf['contrastTextColor'], 'mr-1']"
        >mdi-directions-fork</v-icon
      >
      <span class="mr-2">{{ content.crawl_forks }}</span>
      <span class="mr-1">·</span>
      <v-icon dense :class="[statusConf['contrastTextColor'], 'mr-1']"
        >mdi-note-text-outline</v-icon
      >
      <span class="">{{ content.crawl_issues }}</span>
    </v-card-subtitle>
    <v-card-text
      style="overflow: hidden"
      :class="statusConf['contrastTextColor']"
    >
      {{ content.description }}
    </v-card-text>
    <v-card-actions class="mt-auto" style="width: 100%; min-width: 100%">
      <v-select
        v-model="repoStatus"
        :items="statusList"
        :class="statusConf['contrastTextColor']"
        :color="statusConf['contrastColor']"
        full-width
        dense
      >
        <template slot="selection" slot-scope="{ item }">
          {{ item.text }}
        </template>
      </v-select>
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
    repoStatus: function (val) {
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
    statusConf: function () {
      if (MapRepositoryStatus.has(this.repoStatus))
        return MapRepositoryStatus.get(this.repoStatus);
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
