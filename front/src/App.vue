<template>
  <v-app>
    <v-navigation-drawer v-model="drawer" app clipped stateless>
      <v-list>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title class="title">
              Categories
              <v-btn
                color="primary"
                v-on:click="fetchCategories"
                fab
                small
                absolute
                bottom
                right
              >
                <v-icon>mdi-refresh</v-icon>
              </v-btn>
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <v-divider></v-divider>
      <v-list flat>
        <v-list-item-group
          v-if="categories"
          v-model="categoryIndex"
          color="primary"
          mandatory
        >
          <v-list-item v-for="item in categories" :key="item.id">
            <v-list-item-content>
              <v-list-item-title v-text="item.name"></v-list-item-title>
              <v-list-item-subtitle v-if="'status' in item" align="center">
                <StatusLabel
                  v-for="st in repositoryStatus"
                  :key="st.id"
                  :icon="st.icon"
                  :label="
                    st.id in item['status']
                      ? item['status'][st.id].toString()
                      : '0'
                  "
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
      <v-container v-if="categories" fluid class="pa-0">
        <RepoList v-bind:category="categoryId" />
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
    this.fetchCategories();
  },
  methods: {
    fetchCategories: function() {
      let selectedCategory = this.categoryId;

      this.categories = null;

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

          let selectedCategoryIndex = this.categories.findIndex(
            (elt) => elt.id == selectedCategory
          );

          if (selectedCategoryIndex >= 0)
            this.categoryIndex = selectedCategoryIndex;
          else this.categoryIndex = 0;
        });
    },
  },
  computed: {
    categoryId: function() {
      if (
        this.categoryIndex != null &&
        this.categories != null &&
        this.categoryIndex < this.categories.length
      )
        return this.categories[this.categoryIndex].id;

      return null;
    },
  },
};
</script>
