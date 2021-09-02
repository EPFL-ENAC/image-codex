<template>
  <v-card>
    <v-card-title>Image Tagging</v-card-title>
    <v-card-text>
      <v-file-input
        v-model="images"
        accept="image/jpeg"
        small-chips
        label="Images"
        multiple
        placeholder="Select images"
        prepend-icon="mdi-image"
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
          open-on-click
          selectable
          selection-type="independent"
        ></v-treeview>
        <v-row class="ma-1">
          <v-chip-group column>
            <v-chip v-for="(selection, i) in selectedTags" :key="i" small>
              {{ selection }}
            </v-chip>
          </v-chip-group>
          <v-btn
            v-if="selectedCategories.length > 0"
            @click="selectedCategories = []"
            icon
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-row>
      </v-sheet>
    </v-card-text>
    <v-card-actions>
      <v-btn
        @click="onTagImages"
        :disabled="images.length == 0 || selectedCategories.length == 0"
        color="primary"
        >Tag Images</v-btn
      >
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";
import download from "downloadjs";
import piexif from "piexifjs";
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
        console.error(`unexpected type ${type} for key ${id.join(".")}`);
        return [];
      }
    });
  }

  blobToBase64(blob: Blob): Promise<string | ArrayBuffer | null> {
    return new Promise((resolve) => {
      const reader = new FileReader();
      reader.onloadend = () => resolve(reader.result);
      reader.readAsDataURL(blob);
    });
  }

  onTagImages(): void {
    const tags = this.selectedTags.join(", ");
    this.images.forEach((image) => this.tagImage(image, tags));
  }

  tagImage(image: File, tags: string): void {
    this.blobToBase64(image).then((data) => {
      const oldExifObj = piexif.load(data);
      oldExifObj["0th"][piexif.ImageIFD.ImageDescription] = tags;
      oldExifObj["Exif"][piexif.ExifIFD.UserComment] = tags;
      const exifbytes = piexif.dump(oldExifObj);
      const exifObj = piexif.insert(exifbytes, data);
      download(exifObj, image.name, image.type);
    });
  }
}

interface Item {
  id: string;
  name: string;
  children?: Item[];
}
</script>
