<template>
  <v-container>
    <h1>Image Codex</h1>
    <images-map></images-map>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";
import ImagesMap from "@/components/ImagesMap.vue";

@Component({
  components: {
    ImagesMap,
  },
})
export default class Home extends Vue {}
</script>
