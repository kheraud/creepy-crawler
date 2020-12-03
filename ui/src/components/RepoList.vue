<template>
  <div>
    <v-pagination
      v-model="page"
      :length="4"
    ></v-pagination>
    <v-select v-model="filter" :items="sortList" />
    <v-select v-model="sorting" :items="statusList" />
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
  </div>
</template>
<script>
import Repository from "./Repository.vue";
import { SelectRepositorySort, SelectRepositoryStatus, RepositoryPerPage } from "../utils/enumerations.js";

export default {
  components: {
    Repository,
  },
  props: {
    pageId: Number,
  },
  data() {
    return {
      repositoryPerPage: RepositoryPerPage,
      sorting: 'stars',
      filter: null,
      repos: null,
      sortList: SelectRepositorySort,
      statusList: SelectRepositoryStatus,
      page: 1,
    };
  },
  watch: {
    pageId: function() {
      this.fetchList();
    },
    sorting: function() {
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
          value: this.pageId,
        },
        {
          key: "sort",
          value: this.sorting,
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
        .then((data) => (this.repos = data));
    },
  },
  mounted() {
    this.fetchList();
  },
};
</script>
