<template>
  <v-container>
    <h1>Image Codex</h1>
    <territory-map></territory-map>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";
import TerritoryMap from "@/components/TerritoryMap.vue";

@Component({
  components: {
    TerritoryMap,
  },
})
export default class Territory extends Vue {}
</script>
