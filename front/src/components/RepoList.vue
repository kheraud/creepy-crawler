<template>
  <v-card flat class="ma-0 pa-0" :loading="loading">
    <v-pagination
      v-if="pageCount"
      @input="fetchList(false)"
      v-model="page"
      :length="pageCount"
      total-visible="7"
      class="mt-4"
    ></v-pagination>
    <v-container fluid>
      <v-row align="center">
        <v-col class="d-flex" cols="12" sm="6">
          <v-select
            v-model="sort"
            :items="sortList"
            label="Sort"
            v-on:change="fetchList(true)"
          />
        </v-col>
        <v-col class="d-flex" cols="12" sm="6">
          <v-select
            v-model="statuses"
            :items="statusList"
            @change="fetchList(true)"
            label="Status"
            multiple
            clearable
            placeholder="All"
          />
        </v-col>
      </v-row>
    </v-container>
    <div v-if="repos !== null" class="d-flex justify-space-around flex-wrap">
      <Repository v-for="repo in repos" :key="repo.name" :content="repo" />
    </div>
    <v-pagination
      v-if="pageCount"
      @input="fetchList(false)"
      v-model="page"
      :length="pageCount"
      total-visible="7"
    ></v-pagination>
  </v-card>
</template>
<script>
import Repository from "./Repository.vue";
import {
  SelectRepositorySort,
  SelectRepositoryStatus,
  RepositoryPerPage,
} from "../utils/enumerations.js";

export default {
  components: {
    Repository,
  },
  props: {
    category: Number,
  },
  data() {
    return {
      loading: true,

      repositoryPerPage: RepositoryPerPage,
      sortList: SelectRepositorySort,
      statusList: SelectRepositoryStatus,

      sort: SelectRepositorySort[0].value,
      statuses: null,

      repos: [],
      page: 1,
      pageCount: null,
    };
  },
  watch: {
    category: function() {
      this.fetchList(true);
    },
  },
  methods: {
    fetchList: function(forcePageRewind) {
      this.loading = true;

      let statusQuery = [];

      if (this.statuses != null) {
        statusQuery = this.statuses.map((x) => {
          return {
            key: "status",
            value: x,
          };
        });
      }

      let queryParameters = [
        {
          key: "page",
          value: this.category,
        },
        {
          key: "sort",
          value: this.sort,
        },
        {
          key: "limit",
          value: RepositoryPerPage,
        },
        {
          key: "offset",
          value: forcePageRewind ? 0 : ((this.page - 1) * RepositoryPerPage),
        },
        ...statusQuery,
      ];

      let query = queryParameters
        .filter((x) => x.value != null)
        .map((x) => x.key + "=" + x.value)
        .join("&");

      fetch("/api/repos?" + query)
        .then((response) => response.json())
        .then((data) => {
          this.repos = data["results"];
  
          if (forcePageRewind)
            this.page = 1;

          console.log(forcePageRewind);

          if (data["metadata"]["limit"] > 0)
            this.pageCount = Math.ceil(
              data["metadata"]["total"] / Math.min(data["metadata"]["limit"])
            );

          this.loading = false;
        });
    },
  },
  mounted() {
    this.fetchList(true);
  },
};
</script>
