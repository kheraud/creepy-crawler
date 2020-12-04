<template>
  <div>
    <v-pagination
      v-if="pageCount"
      v-model="page"
      :length="pageCount"
      total-visible="7"
    ></v-pagination>
    <v-select v-model="sort" :items="sortList" />
    <v-select v-model="statuses" :items="statusList" />
    <div v-if="repos !== null" class="d-flex justify-space-around flex-wrap">
      <Repository v-for="repo in repos" :key="repo.name" :content="repo" />
    </div>
    <div v-else class="d-flex justify-space-around flex-wrap">
      <v-skeleton-loader
        v-for="n in repositoryPerPage"
        :key="n"
        elevation="1"
        type="article, actions"
        width="400"
        class="ma-1"
      />
    </div>
    <v-pagination
      v-if="pageCount"
      v-model="page"
      :length="pageCount"
      total-visible="7"
    ></v-pagination>
  </div>
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
      repositoryPerPage: RepositoryPerPage,
      sortList: SelectRepositorySort,
      statusList: SelectRepositoryStatus,

      sort: SelectRepositorySort[0],
      statuses: null,

      repos: null,
      page: 1,
      pageCount: null,
    };
  },
  watch: {
    category: function() {
      this.page = 1;
      this.pageCount = null;
      this.fetchList();
    },
    sort: function() {
      this.fetchList();
    },
    page: function() {
      this.fetchList();
    },
  },
  methods: {
    fetchList: function() {
      this.repos = null;
      let query = [
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
          value: (this.page - 1) * RepositoryPerPage,
        },
      ]
        .filter((x) => x.value != null)
        .map((x) => x.key + "=" + x.value)
        .join("&");

      fetch("/api/repos?" + query)
        .then((response) => response.json())
        .then((data) => {
          this.repos = data["results"];
          if (data["metadata"]["limit"] > 0) {
            this.pageCount = Math.ceil(
              data["metadata"]["total"] / Math.min(data["metadata"]["limit"])
            );
          }
        });
    },
  },
  mounted() {
    this.fetchList();
  },
};
</script>
