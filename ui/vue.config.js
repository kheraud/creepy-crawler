module.exports = {
  "outputDir": "../dist",
  "assetsDir": "static",
  "devServer": {
    "proxy": "http://localhost:5000"
  },
  "transpileDependencies": [
    "vuetify"
  ]
}