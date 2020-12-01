<template>
  <tbody>
    <tr :id="content.id">
      <td align="center">{{ content.crawl_stars }}</td>
      <td align="center">{{ content.crawl_forks }}</td>
      <td align="center">{{ content.crawl_issues }}</td>
      <td><a :href="content.url" target="_blank">{{ content.name }}</a></td>
    </tr>
    <tr>
      <td colspan="4"><small>{{ content.description }}</small></td>
    </tr>
  </tbody>
</template>
<script>
export default {
  props: {
    content: Object,
  },
};
</script>
