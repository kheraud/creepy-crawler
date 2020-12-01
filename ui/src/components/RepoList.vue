<template>
  <div>
    <table v-if="repos != null">
      <thead>
        <tr>
          <th align="center">Stars</th>
          <th align="center">Forks</th>
          <th align="center">Issues</th>
          <th>Name</th>
        </tr>
      </thead>
      <Repository v-for="repo in repos" :key="repo.name" :content="repo" />
    </table>
    <div v-else>
      sddd
    </div>
  </div>
</template>
<script>
import Repository from "./Repository.vue";

export default {
  components: {
    Repository,
  },
  props: {
    pageId: Number,
  },
  data() {
    return {
      repos: null,
    };
  },
  watch: {
    pageId: function (newVal) {
      this.fetchList(newVal);
    },
  },
  methods: {
    fetchList: function (pageId) {
      this.repos = null;
      fetch("/api/repos?page=" + pageId)
        .then((response) => response.json())
        .then((data) => (this.repos = data));
    }
  },
  mounted() {
    this.fetchList(this.pageId);
  },
};
</script>
