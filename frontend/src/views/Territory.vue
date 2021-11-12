<template>
  <v-container>
    <v-row>
      <v-col>
        <h1>Territory Map</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <territory-map></territory-map>
      </v-col>
    </v-row>
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
