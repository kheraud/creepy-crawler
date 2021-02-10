<template>
  <v-chip
    :class="['mr-1', statusConf['contrastTextColor']]"
    :color="statusConf['color']"
    small
  >
    <v-icon small class="mr-1">{{ statusConf["icon"] }}</v-icon>
    {{ label }}
  </v-chip>
</template>
<script>
export default {
  props: {
    statusConf: String,
    label: String,
  },
};
</script>
