<template>
  <v-card flat>
    <v-card-title>Image Tagging</v-card-title>
    <v-card-text>
      <v-row>
        <v-col cols="12" sm="8">
          <v-sheet class="ma-1">
            <v-row>
              <v-file-input
                v-model="imageFiles"
                accept="image/jpeg"
                small-chips
                label="Select Images"
                multiple
                prepend-icon="mdi-image"
                show-size
                @change="onChangeImages"
              ></v-file-input>
            </v-row>
            <v-row>
              <v-col v-for="(image, i) in images" :key="i">
                <image-item ref="imageItems" v-model="images[i]"></image-item>
              </v-col>
            </v-row>
          </v-sheet>
        </v-col>
        <v-col cols="12" sm="4">
          <v-sheet class="ma-1">
            <v-row>
              <v-text-field
                v-model="search"
                label="Search Categories"
                hide-details
                clearable
              ></v-text-field>
            </v-row>
            <v-row>
              <v-chip-group column>
                <v-chip
                  v-for="(tag, i) in selectedTags"
                  :key="i"
                  close
                  @click:close="onCloseTag(tag)"
                >
                  {{ tag }}
                </v-chip>
              </v-chip-group>
            </v-row>
            <v-row>
              <v-treeview
                v-model="selectedCategories"
                :items="treeCategories"
                :search="search"
                hoverable
                open-on-click
                selectable
                selected-color="primary"
                selection-type="independent"
              ></v-treeview>
            </v-row>
            <v-row>
              <v-btn
                color="primary"
                :disabled="selectedCategories.length == 0 || images.length == 0"
                @click="onClickAddTags"
              >
                Add to images
                <v-icon right>mdi-plus-circle</v-icon>
              </v-btn>
            </v-row>
          </v-sheet>
        </v-col>
      </v-row>
    </v-card-text>
    <v-card-actions>
      <v-btn
        :disabled="imageFiles.length == 0"
        color="primary"
        @click="onClickTagImages"
        >Tag Images</v-btn
      >
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";
import download from "downloadjs";
import categories from "../assets/categories.yaml";
import ImageItem from "./ImageItem.vue";
import Image from "@/models/image";

@Component({
  components: {
    ImageItem,
  },
})
export default class ImageUpload extends Vue {
  readonly tagSeparator = ", ";

  search = "";
  selectedCategories: string[] = [];
  imageFiles: File[] = [];
  images: Image[] = [];

  get treeCategories(): Item[] {
    return this.parseTree(categories);
  }

  get selectedTags(): string[] {
    return this.selectedCategories
      .flatMap((categories) => categories.split(this.tagSeparator))
      .filter((v, i, a) => a.indexOf(v) === i)
      .sort();
  }

  // eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types, @typescript-eslint/no-explicit-any
  parseTree(obj: any, parents: string[] = []): Item[] {
    return Object.entries(obj).flatMap(([key, value]) => {
      const id = [...parents, key];
      const type = typeof value;
      if (type === "object") {
        if (value === null) {
          return [
            {
              id: id.join(this.tagSeparator),
              name: key,
            },
          ];
        } else {
          return [
            {
              id: id.join(this.tagSeparator),
              name: key,
              children: this.parseTree(value, id),
            },
          ];
        }
      } else {
        console.error(`unexpected type ${type} for key ${id.join(".")}`);
        return [];
      }
    });
  }

  mapFileToBase64(blob: Blob): Promise<string> {
    return new Promise((resolve) => {
      const reader = new FileReader();
      reader.onloadend = () => resolve(reader.result as string);
      reader.readAsDataURL(blob);
    });
  }

  onChangeImages(): void {
    const files = this.imageFiles;
    Promise.all(files.map(this.mapFileToBase64)).then((contents) => {
      return (this.images = contents.map(
        (content, i) => new Image(files[i], content)
      ));
    });
  }

  onClickTagImages(): void {
    this.images.forEach((image) => {
      const content = image.tag(this.tagSeparator);
      download(content, image.name, image.type);
    });
  }

  onCloseTag(tag: string): void {
    this.selectedCategories = this.selectedCategories.filter((category) => {
      return !category.split(this.tagSeparator).some((t) => t === tag);
    });
  }

  onClickAddTags(): void {
    const tags = this.selectedTags;
    this.images.forEach((image) => {
      image.addTags(tags);
    });
    const imageItems: Vue[] = this.$refs.imageItems as Vue[];
    imageItems.forEach((item) => {
      item.$forceUpdate();
    });
  }
}

interface Item {
  id: string;
  name: string;
  children?: Item[];
}
</script>
