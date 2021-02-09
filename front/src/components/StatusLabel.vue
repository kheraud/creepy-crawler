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
    return {
      textColor: this.colorRef
        .split(" ")
        .map((col) => {
          if (col.startsWith("lighten") || col.startsWith("darken"))
            return "text--" + col;
          return col + "--text";
        })
        .join(" "),
    };
  },
};
</script>
