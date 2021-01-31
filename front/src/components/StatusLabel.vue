<template>
  <span :class="['mr-1', textColor]">
    <v-icon small class="ml-2" :color="colorRef">{{ icon }}</v-icon>
    {{ label }}
  </span>
</template>
<script>
export default {
  props: {
    icon: String,
    label: String,
    colorRef: String,
  },
  data() {
    let sColor = this.colorRef.split(" ");
    sColor[0] = sColor[0] + "--text";
    return {
      textColor: sColor.join(" "),
    };
  },
};
</script>
