<template>
  <v-container>
    <image-upload />
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import ImageUpload from "../components/ImageUpload.vue";

export default Vue.extend({
  name: "Home",

  components: {
    ImageUpload,
  },
});
</script>
