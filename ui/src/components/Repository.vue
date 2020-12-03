<template>
  <v-card
    elevation="1"
    width="400"
    height="250"
    class="d-flex flex-column align-start ma-1"
  >
    <v-card-title>
      {{ content.name }}
    </v-card-title>
    <v-card-subtitle>
      <v-icon class="mr-1">mdi-link-variant</v-icon>
      <a :href="content.url" target="_blank" class="mr-1">View</a>
      <span class="mr-1">·</span>
      <v-icon class="mr-1">mdi-heart</v-icon>
      <span class=" mr-2">{{ content.crawl_stars }}</span>
      <span class="mr-1">·</span>
      <v-icon class="mr-1">mdi-directions-fork</v-icon>
      <span class=" mr-2">{{ content.crawl_forks }}</span>
      <span class="mr-1">·</span>
      <v-icon class="mr-1">mdi-note-text-outline</v-icon>
      <span class="">{{ content.crawl_issues }}</span>
    </v-card-subtitle>
    <v-card-text style="overflow: hidden">
      {{ content.description }}
    </v-card-text>
    <v-card-actions class="d-flex flex-column mt-auto" style="width: 100%">
      <v-select
        v-model="repoStatus"
        :items="statusList"
        label="Statut"
        rounded
        :background-color="statusColor"
        full-width
        dense
      />
    </v-card-actions>
  </v-card>
</template>
<script>
import {
  RepositoryStatus,
  SelectRepositoryStatus,
} from "../utils/enumerations.js";

export default {
  props: {
    content: Object,
  },
  data() {
    return {
      repoStatus: this.content.status,
      statusList: SelectRepositoryStatus,
    }
  },
  computed: {
    statusColor: function() {
      if (this.repoStatus != null && Object.prototype.hasOwnProperty.call(RepositoryStatus, this.repoStatus)) {
        return RepositoryStatus[this.repoStatus]['color']
      } else {
        return undefined
      }
    },
  }
};
</script>
