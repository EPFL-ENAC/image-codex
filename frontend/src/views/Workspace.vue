<template>
  <v-row>
    <v-col cols="8">
      <v-sheet class="ma-4" min-height="256px" elevation="4">
        <v-toolbar color="secondary">
          <v-row>
            <v-col>
              <v-text-field
                v-model.number="columnsCount"
                label="Columns"
                type="number"
                dark
                hide-details
              ></v-text-field>
            </v-col>
            <v-col>
              <v-switch
                v-model="layoutFlat"
                label="Flat"
                dark
                hide-details
              ></v-switch>
            </v-col>
          </v-row>
        </v-toolbar>
        <grid-layout
          :layout.sync="layout"
          :col-num="columnsCount"
          :row-height="32"
          :is-draggable="true"
          :is-resizable="true"
          :vertical-compact="false"
          :prevent-collision="true"
        >
          <grid-item
            v-for="item in layout"
            :key="item.i"
            :x="item.x"
            :y="item.y"
            :w="item.w"
            :h="item.h"
            :i="item.i"
          >
            <v-sheet
              class="d-flex align-content-center"
              :elevation="layoutElevation"
              height="100%"
              width="100%"
            >
              <v-img
                :src="item.value.url"
                max-height="100%"
                max-width="100%"
                contain
              ></v-img>
            </v-sheet>
          </grid-item>
        </grid-layout>
      </v-sheet>
    </v-col>
    <v-col cols="4">
      <image-browser @add="addImage"></image-browser>
    </v-col>
  </v-row>
</template>

<style scoped>
.vue-grid-item {
  touch-action: none;
}
</style>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";
import ImageBrowser from "@/components/ImageBrowser.vue";
import BackendImage from "@/models/backend-image";
import { GridLayout, GridItem } from "vue-grid-layout";

@Component({
  components: {
    ImageBrowser,
    GridLayout,
    GridItem,
  },
})
export default class Workspace extends Vue {
  columnsCount = 12;
  layoutFlat = false;
  images: BackendImage[] = [];
  layout: Layout<BackendImage>[] = [];

  get layoutElevation(): number {
    return this.layoutFlat ? 0 : 1;
  }

  addImage(image: BackendImage): void {
    this.images.push(image);
    this.layout.push({
      x: 0,
      y: 0,
      w: 2,
      h: 2,
      i: this.layout.length,
      value: image,
    });
  }
}

interface Layout<T> {
  x: number;
  y: number;
  w: number;
  h: number;
  i: number;
  value: T;
}
</script>
