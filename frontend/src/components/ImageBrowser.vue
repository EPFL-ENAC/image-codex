<template>
  <v-card flat>
    <v-card-text>
      <v-combobox
        v-model="selectedTags"
        :items="tags"
        label="Tags"
        chips
        clearable
        deletable-chips
        multiple
        @change="initializeImages"
      ></v-combobox>
      <v-row>
        <v-col v-for="item in images" :key="item.id" cols="12" sm="12" md="6">
          <v-card>
            <v-img :src="item.url"></v-img>
            <v-chip-group class="mx-2" column>
              <v-chip
                v-for="tag in item.tags"
                :color="getTagColor(tag)"
                :key="tag"
                small
              >
                {{ tag }}
              </v-chip>
            </v-chip-group>
          </v-card>
        </v-col>
        <v-col v-if="next">
          <v-badge color="secondary" :content="remainingImagesCount" overlap>
            <v-btn color="primary" fab small @click="getNextImages">
              <v-icon>mdi-dots-horizontal</v-icon>
            </v-btn>
          </v-badge>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";
import categories from "@/assets/categories.yaml";
import CursorPage from "@/models/cursorPage";
import { paramsSerializer, unique } from "@/utils/functions";

@Component
export default class ImageBrowser extends Vue {
  selectedTags: string[] = [];
  images: LinkImage[] = [];
  readonly pageSize = 4;
  next: string | undefined = undefined;
  imagesCount = 0;

  get tags(): string[] {
    return this.getItems(categories).filter(unique).sort();
  }

  get remainingImagesCount(): number {
    return this.imagesCount - this.images.length;
  }

  created(): void {
    this.initializeImages();
  }

  getTagColor(tag: string): string | undefined {
    return this.selectedTags.includes(tag) ? "secondary" : undefined;
  }

  getItems(obj: unknown): string[] {
    return Object.entries(obj as Record<string, unknown>).flatMap(
      ([key, value]) => {
        const type = typeof value;
        if (type === "object") {
          if (value === null) {
            return [key];
          } else {
            return [key].concat(this.getItems(value));
          }
        } else {
          console.error(`unexpected type ${type} for key ${key}`);
          return [];
        }
      }
    );
  }

  private updateItems(callback: (images: LinkImage[]) => void) {
    this.$http
      .get<CursorPage<LinkImage>>("/images", {
        params: {
          size: this.pageSize,
          next: this.next,
          tags: this.selectedTags,
        },
        paramsSerializer: paramsSerializer,
      })
      .then((response) => {
        this.next = response.data.next;
        this.imagesCount = response.data.total;
        callback(response.data.items);
      });
  }

  initializeImages(): void {
    this.next = undefined;
    this.images = [];
    this.getNextImages();
  }

  getNextImages(): void {
    this.updateItems((images) => this.images.push(...images));
  }
}

interface LinkImage {
  id: string;
  name: string;
  url: string;
  author: string;
  license: string;
}
</script>
