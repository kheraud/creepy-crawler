<template>
  <v-app>
    <v-navigation-drawer v-model="drawer" app clipped stateless>
      <v-list shaped>
        <v-subheader>Categories</v-subheader>
        <v-list-item-group
          v-if="categories"
          v-model="categoryIndex"
          color="primary"
        >
          <v-list-item v-for="item in categories" :key="item.id">
            <v-list-item-content>
              <v-list-item-title v-text="item.name"></v-list-item-title>
              <v-list-item-subtitle v-if="'status' in item" align="center">
                <StatusLabel
                  v-for="st in repositoryStatus"
                  :key="st.id"
                  :icon="st.icon"
                  :label="st.id in item['status'] ? item['status'][st.id] : 0"
                  :color-ref="st.color"
                >
                </StatusLabel>
              </v-list-item-subtitle>
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
import FullLoader from "./components/FullLoader.vue";
import StatusLabel from "./components/StatusLabel";
import { RepositoryStatus } from "./utils/enumerations.js";
import RepoList from "./components/RepoList.vue";
import Footer from "./components/Footer.vue";

export default {
  data() {
    return {
      categoryIndex: 0,
      categories: null,
      drawer: true,
      repositoryStatus: RepositoryStatus,
    };
  },
  components: {
    RepoList,
    Footer,
    FullLoader,
    StatusLabel,
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
