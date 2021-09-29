<template>
  <v-container>
    <image-upload />
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";
import ImageUpload from "../components/ImageUpload.vue";

@Component({
  components: {
    ImageUpload,
  },
})
export default class Upload extends Vue {}
</script>
