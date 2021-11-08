<template>
  <v-container>
  <div >
    <h1>Territory Map</h1>
    </div>
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
