<template>
  <v-app>
    <v-app-bar app>
      Bar
    </v-app-bar>
    <v-main>
      <v-container fluid>
        <v-select v-model="pageId" :items="pageList" />
        <RepoList v-bind:page-id="pageId" />
      </v-container>
    </v-main>
    <v-footer app>
      Footer here
    </v-footer>
  </v-app>
</template>

<script>
import RepoList from "./components/RepoList.vue";

export default {
  data() {
    return {
      pageId: null,
      pageList: [],
    }
  },
  components: {
    RepoList,
  },
  mounted() {
    fetch("/api/pages")
      .then((response) => response.json())
      .then((data) => {
        this.pageList = [{
          text: "-- All pages --",
          value: null
        }]
        data.forEach(element => {
          this.pageList.push({
            text: element.name + ' (' + element.count + ')',
            value: element.id
          })
        });
      });
  },
};
</script>
