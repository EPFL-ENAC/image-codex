<template>
  <v-row>
    <v-col cols="8">
      <v-skeleton-loader type="article" boilerplate></v-skeleton-loader>
    </v-col>
    <v-col cols="4">
      <image-browser></image-browser>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";
import ImageBrowser from "@/components/ImageBrowser.vue";

@Component({
  components: {
    ImageBrowser,
  },
})
export default class Workspace extends Vue {}
</script>
