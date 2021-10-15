<template>
  <v-card color="secondary" dark>
    <v-card-title>
      <v-text-field
        v-model="composition.name"
        label="Name"
        hide-details
      ></v-text-field>
    </v-card-title>
    <v-card-subtitle>
      <v-row>
        <v-col>
          <v-text-field
            v-model.number="composition.height"
            label="Height"
            suffix="px"
            type="number"
            hide-details
          ></v-text-field>
        </v-col>
        <v-col>
          <v-text-field
            v-model.number="composition.width"
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
            v-for="(image, index) in composition.images"
            :key="composition.width + '-' + composition.height + '-' + index"
            :x="image.x"
            :y="image.y"
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
      <v-btn :disabled="!isValid" color="primary" @click="downloadComposition">
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
import { ApiFile, RequestComposition, ResponseImage } from "@/backend";
import download from "downloadjs";
import { LocalStorageKey } from "@/utils/contants";

@Component
export default class CompositionEditor extends Vue {
  composition: RequestComposition = CompositionEditor.getCompositionOrDefault();

  private static getCompositionOrDefault(): RequestComposition {
    const value = localStorage.getItem(LocalStorageKey.Composition);
    if (value) {
      try {
        return JSON.parse(value) as RequestComposition;
      } catch (exception) {
        localStorage.removeItem(LocalStorageKey.Composition);
      }
    }
    return {
      name: "",
      width: 1123,
      height: 794,
      images: [],
    };
  }

  get parentStyle(): Record<string, unknown> {
    return {
      width: this.composition.width + "px",
      height: this.composition.height + "px",
    };
  }

  get isValid(): boolean {
    return (
      this.composition.name.length > 0 && this.composition.images.length > 0
    );
  }

  updated(): void {
    localStorage.setItem(
      LocalStorageKey.Composition,
      JSON.stringify(this.composition)
    );
  }

  public addImage(image: ResponseImage): void {
    const maxInitSize = 200;
    const ratio = Math.max(image.width, image.height) / maxInitSize;
    this.composition.images.push({
      id: image.id,
      url: image.url,
      x: 0,
      y: 0,
      width: image.width / ratio,
      height: image.height / ratio,
    });
  }

  onDrag(index: number, x: number, y: number): void {
    this.composition.images[index].x = x;
    this.composition.images[index].y = y;
  }

  onResize(
    index: number,
    x: number,
    y: number,
    width: number,
    height: number
  ): void {
    this.composition.images[index].x = x;
    this.composition.images[index].y = y;
    this.composition.images[index].width = width;
    this.composition.images[index].height = height;
  }

  downloadComposition(): void {
    this.$http
      .post<ApiFile>("/compositions", this.composition)
      .then((response) => {
        const file = response.data;
        // https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URIs
        download(
          `data:${file.type};base64,${file.base64}`,
          file.name,
          file.type
        );
      });
  }
}
</script>
