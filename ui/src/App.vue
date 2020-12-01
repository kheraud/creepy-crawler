<template>
  <div>
    <section class="section">
      <select v-model="pageId">
        <option disabled value="">-- Select a page --</option>
        <option v-for="page in pages" v-bind:key="page.id" v-bind:value="page.id">
          {{ page.name }}
        </option>
      </select>
      <RepoList v-bind:page-id="pageId" />
    </section>
  </div>
</template>

<script>
import RepoList from "./components/RepoList.vue";

export default {
  data() {
    return {
      pageId: null,
      pages: []
    }
  },
  components: {
    RepoList,
  },
  mounted() {
    fetch("/api/pages")
      .then((response) => response.json())
      .then((data) => (this.pages = data));
  },

};
</script>
