module.exports = {
  "outputDir": process.env.DIST_DIR,
  "assetsDir": "static",
  "devServer": {
    "port": 8080,
    "proxy": process.env.PROXY_API
  },
  "transpileDependencies": [
    "vuetify"
  ]
}