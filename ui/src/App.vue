<template>
  <v-app>
    <v-navigation-drawer v-model="drawer" app clipped stateless>
      <v-list shaped>
        <v-subheader>Categories</v-subheader>
        <v-list-item-group v-if="categories" v-model="categoryIndex" color="primary">
          <v-list-item v-for="item in categories" :key="item.id">
            <v-list-item-content>
              <v-list-item-title v-text="item.name"></v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
        <FullLoader v-else />
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>Creepy Crawler</v-toolbar-title>
    </v-app-bar>

    <v-main>
      <v-container v-if="categories" fluid>
        <RepoList v-bind:category="categories[categoryIndex].id" />
      </v-container>
      <FullLoader v-else />
    </v-main>
    <Footer />
  </v-app>
</template>

<script>
import RepoList from "./components/RepoList.vue";
import Footer from "./components/Footer.vue";
import FullLoader from "./components/FullLoader.vue"

export default {
  data() {
    return {
      categoryIndex: 0,
      categories: null,
      drawer: true,
    };
  },
  components: {
    RepoList,
    Footer,
    FullLoader,
  },
  mounted() {
    fetch("/api/pages")
      .then((response) => response.json())
      .then((data) => {
        this.categories = [
          {
            id: null,
            name: "All",
          },
          ...data,
        ];
      });
  },
};
</script>
