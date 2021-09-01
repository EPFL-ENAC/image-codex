<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-file-input
          v-model="images"
          accept="image/png, image/jpeg, image/bmp"
          small-chips
          label="Image"
          multiple
          placeholder="Select an image"
          prepend-icon="mdi-camera"
          show-size
        ></v-file-input>
        <v-sheet>
          <v-text-field
            v-model="search"
            label="Search Categories"
            hide-details
            clearable
          ></v-text-field>
          <v-treeview
            v-model="selectedCategories"
            :items="treeCategories"
            :search="search"
            selectable
            selection-type="independent"
          ></v-treeview>
          <v-chip
            v-for="(selection, i) in selectedTags"
            :key="i"
            small
            class="ma-1"
          >
            {{ selection }}
          </v-chip>
        </v-sheet>
        <v-btn
          v-on:click="tagImages"
          color="primary"
          :disabled="images.length == 0 || selectedCategories.length == 0"
          >Tag Image</v-btn
        >
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";
import categories from "../assets/categories.yaml";

@Component
export default class ImageUpload extends Vue {
  search = "";
  selectedCategories: string[] = [];
  separator = ";";
  images: File[] = [];

  get treeCategories(): Item[] {
    return this.parseTree(categories);
  }

  get selectedTags(): string[] {
    return this.selectedCategories
      .flatMap((categories) => categories.split(this.separator))
      .filter((v, i, a) => a.indexOf(v) === i);
  }

  parseTree(obj: unknown, parents: string[] = []): Item[] {
    return Object.entries(obj).flatMap(([key, value]) => {
      if (typeof value === "object") {
        const id = [...parents, key];
        if (value === null) {
          return [
            {
              id: id.join(this.separator),
              name: key,
            },
          ];
        } else {
          return [
            {
              id: id.join(this.separator),
              name: key,
              children: this.parseTree(value, id),
            },
          ];
        }
      } else {
        return [];
      }
    });
  }

  tagImages(): void {
    this.images.forEach((image) => {
      console.log(image);
    });
  }
}

interface Item {
  id: string;
  name: string;
  children?: Item[];
}
</script>
