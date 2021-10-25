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
        <v-col>
          <v-switch
            v-model="showActions"
            label="Show Actions"
            title="Show available actions on each image"
            hide-details
          ></v-switch>
        </v-col>
        <v-col>
          <v-switch
            v-model="showTags"
            label="Show Tags"
            hide-details
          ></v-switch>
        </v-col>
        <v-col>
          <v-text-field
            v-model.number="gridSize"
            label="Grid size"
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
            :key="
              composition.width +
              '-' +
              composition.height +
              '-' +
              index +
              '-' +
              image.id
            "
            :x="image.x"
            :y="image.y"
            :w="image.width"
            :h="image.height"
            :grid="[gridSize, gridSize]"
            :lockAspectRatio="true"
            :parent="true"
            @dragging="(x, y) => dragImage(index, x, y)"
            @resizing="
              (x, y, width, height) => resizeImage(index, x, y, width, height)
            "
          >
            <v-img :src="image.url" contain></v-img>
            <v-speed-dial
              v-if="showActions"
              fixed
              left
              open-on-hover
              top
              direction="bottom"
            >
              <template v-slot:activator>
                <v-btn fab>
                  <v-icon>mdi-dots-horizontal</v-icon>
                </v-btn>
              </template>
              <v-btn title="Delete" fab x-small @click="deleteImage(index)">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
              <v-btn
                title="Move to front"
                fab
                x-small
                @click="flipToFront(index)"
              >
                <v-icon>mdi-flip-to-front</v-icon>
              </v-btn>
              <v-btn
                title="Move to back"
                fab
                x-small
                @click="flipToBack(index)"
              >
                <v-icon>mdi-flip-to-back</v-icon>
              </v-btn>
            </v-speed-dial>
            <v-overlay v-if="showTags">
              <v-chip-group class="mx-2" column>
                <v-chip v-for="tag in getImageTags(image.id)" :key="tag" small>
                  {{ tag }}
                </v-chip>
              </v-chip-group>
            </v-overlay>
          </vue-draggable-resizable>
        </div>
      </div>
    </v-card-text>
    <v-card-actions>
      <v-btn :disabled="!isValid" color="primary" @click="downloadComposition">
        <v-icon left>mdi-download</v-icon>
        Download
      </v-btn>
      <v-btn text @click="resetSize">Reset size</v-btn>
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
import { ApiFile, ComposedImage, Composition, TaggedImage } from "@/backend";
import download from "downloadjs";
import { LocalStorageKey } from "@/utils/contants";

@Component
export default class CompositionEditor extends Vue {
  static readonly defaultWidth = 1123;
  static readonly defaultHeight = 794;
  composition: Composition = this.getCompositionOrDefault();
  showActions = true;
  showTags = false;
  gridSize = 5;
  images: Map<string, TaggedImage> = new Map();

  private getCompositionOrDefault(): Composition {
    const value = localStorage.getItem(LocalStorageKey.Composition);
    if (value) {
      try {
        const composition = JSON.parse(value) as Composition;
        if (composition.images.length > 0) {
          const imageIds = composition.images
            .map((image) => image.id)
            .join(",");
          this.$http
            .get<TaggedImage[]>(`/images/${imageIds}`)
            .then((response) => response.data)
            .then((images) =>
              images.forEach((image) => this.images.set(image.id, image))
            );
        }
        if (!composition.width || composition.width < 0) {
          composition.width = CompositionEditor.defaultWidth;
        }
        if (!composition.height || composition.height < 0) {
          composition.height = CompositionEditor.defaultHeight;
        }
        return composition;
      } catch (exception) {
        localStorage.removeItem(LocalStorageKey.Composition);
      }
    }
    return {
      name: "",
      width: CompositionEditor.defaultWidth,
      height: CompositionEditor.defaultHeight,
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

  public addImage(image: TaggedImage): void {
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
    this.images.set(image.id, image);
  }

  dragImage(index: number, x: number, y: number): void {
    this.composition.images[index].x = x;
    this.composition.images[index].y = y;
  }

  resizeImage(
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

  deleteImage(index: number): ComposedImage[] {
    return this.composition.images.splice(index, 1);
  }

  flipToFront(index: number): void {
    this.composition.images.push(...this.deleteImage(index));
  }

  flipToBack(index: number): void {
    this.composition.images.unshift(...this.deleteImage(index));
  }

  getImageTags(id: string): string[] {
    const image = this.images.get(id);
    if (image) {
      return image.tags;
    } else {
      return [];
    }
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

  resetSize(): void {
    this.composition.width = CompositionEditor.defaultWidth;
    this.composition.height = CompositionEditor.defaultHeight;
  }
}
</script>
