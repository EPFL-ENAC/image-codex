<template>
  <v-row>
    <v-col cols="8">
      <v-sheet class="ma-4" elevation="4">
        <v-toolbar color="secondary">
          <v-row>
            <v-col>
              <v-text-field
                v-model="name"
                label="Name"
                dark
                hide-details
              ></v-text-field>
            </v-col>
            <v-col>
              <v-text-field
                v-model.number="height"
                label="Height"
                suffix="px"
                type="number"
                dark
                hide-details
              ></v-text-field>
            </v-col>
            <v-col>
              <v-text-field
                v-model.number="width"
                label="Width"
                suffix="px"
                type="number"
                dark
                hide-details
              ></v-text-field>
            </v-col>
          </v-row>
        </v-toolbar>
        <div class="background">
          <div class="parent" :style="parentStyle">
            <vue-draggable-resizable
              v-for="(layout, index) in layouts"
              :key="width + '-' + height + '-' + index"
              :w="layout.width"
              :h="layout.height"
              :parent="true"
              :lockAspectRatio="true"
              :grid="[5, 5]"
            >
              <v-img :src="layout.value.url" contain></v-img>
            </vue-draggable-resizable>
          </div>
        </div>
      </v-sheet>
    </v-col>
    <v-col cols="4">
      <image-browser @add="addImage"></image-browser>
    </v-col>
  </v-row>
</template>

<style scoped>
.background {
  overflow: scroll;
  background-color: var(--v-secondary-lighten4);
}
.parent {
  position: relative;
  background-color: white;
}
.draggable {
  border: none;
}
.v-image {
  height: 100%;
}
</style>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";
import ImageBrowser from "@/components/ImageBrowser.vue";
import BackendImage from "@/models/backend-image";

@Component({
  components: {
    ImageBrowser,
  },
})
export default class Workspace extends Vue {
  name = "";
  height = 794;
  width = 1123;
  layouts: Layout<BackendImage>[] = [];

  get parentStyle(): Record<string, unknown> {
    return {
      width: this.width + "px",
      height: this.height + "px",
    };
  }

  addImage(image: BackendImage): void {
    const ratio = Math.max(image.width, image.height) / 200;
    this.layouts.push({
      x: 0,
      y: 0,
      width: image.width / ratio,
      height: image.height / ratio,
      value: image,
    });
  }
}

interface Layout<T> {
  x: number;
  y: number;
  width: number;
  height: number;
  value: T;
}
</script>
