<template>
  <v-container>
    <h1>Image Codex</h1>
    <territory-map></territory-map>
  </v-container>
</template>

<script lang="ts">
import TerritoryMap from "@/components/TerritoryMap.vue";
import Vue from "vue";
import Component from "vue-class-component";

@Component({
  components: {
    TerritoryMap,
  },
})
export default class Territory extends Vue {}
</script>
