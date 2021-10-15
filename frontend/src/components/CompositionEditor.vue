<template>
  <v-card color="secondary" dark>
    <v-card-title>
      <v-text-field v-model="name" label="Name" hide-details></v-text-field>
    </v-card-title>
    <v-card-subtitle>
      <v-row>
        <v-col>
          <v-text-field
            v-model.number="height"
            label="Height"
            suffix="px"
            type="number"
            hide-details
          ></v-text-field>
        </v-col>
        <v-col>
          <v-text-field
            v-model.number="width"
            label="Width"
            suffix="px"
            type="number"
            hide-details
          ></v-text-field>
        </v-col>
      </v-row>
    </v-card-subtitle>
    <v-card-text>
      <div class="background">
        <div class="parent" :style="parentStyle">
          <vue-draggable-resizable
            v-for="(image, index) in images"
            :key="width + '-' + height + '-' + index"
            :w="image.width"
            :h="image.height"
            :grid="[5, 5]"
            :lockAspectRatio="true"
            :parent="true"
            @dragging="(x, y) => onDrag(index, x, y)"
            @resizing="
              (x, y, width, height) => onResize(index, x, y, width, height)
            "
          >
            <v-img :src="image.url" contain></v-img>
          </vue-draggable-resizable>
        </div>
      </div>
    </v-card-text>
    <v-card-actions>
      <v-btn
        :disabled="!name || !images"
        color="primary"
        @click="downloadComposition"
      >
        <v-icon left>mdi-download</v-icon>
        Download
      </v-btn>
    </v-card-actions>
  </v-card>
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
import { ApiFile, ComposedImage, RequestComposition } from "@/backend";
import download from "downloadjs";

const CompositionEditorProps = Vue.extend({
  props: {
    images: Array as () => ComposedImage[],
  },
});

@Component
export default class CompositionEditor extends CompositionEditorProps {
  name = "";
  height = 794;
  width = 1123;
  get parentStyle(): Record<string, unknown> {
    return {
      width: this.width + "px",
      height: this.height + "px",
    };
  }
  onDrag(index: number, x: number, y: number): void {
    this.images[index].x = x;
    this.images[index].y = y;
  }
  onResize(
    index: number,
    x: number,
    y: number,
    width: number,
    height: number
  ): void {
    this.images[index].x = x;
    this.images[index].y = y;
    this.images[index].width = width;
    this.images[index].height = height;
  }
  downloadComposition(): void {
    const composition: RequestComposition = {
      name: this.name,
      width: this.width,
      height: this.height,
      images: this.images,
    };
    this.$http.post<ApiFile>("/compositions", composition).then((response) => {
      const file = response.data;
      // https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URIs
      download(`data:${file.type};base64,${file.base64}`, file.name, file.type);
    });
  }
}
</script>
