<template>
  <v-card>
    <v-card-title>Image Tagging</v-card-title>
    <v-card-text>
      <v-file-input
        v-model="imageFiles"
        @change="onChangeImages"
        accept="image/jpeg"
        small-chips
        label="Select Images"
        multiple
        prepend-icon="mdi-image"
        show-size
      ></v-file-input>
      <v-row>
        <v-col v-for="(file, i) in imageFiles" :key="i">
          <v-img
            :src="images[i].content"
            :lazy-src="file.name"
            contain
            max-height="256"
            max-width="256"
          >
            <template v-slot:placeholder>
              <v-row class="fill-height ma-0" align="center" justify="center">
                <v-progress-circular
                  indeterminate
                  color="primary"
                ></v-progress-circular>
              </v-row> </template
          ></v-img>
        </v-col>
      </v-row>

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
        @click="onClickTagImages"
        :disabled="imageFiles.length == 0 || selectedCategories.length == 0"
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
  imageFiles: File[] = [];
  images: Image[] = [];

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
    const tags = this.selectedTags.join(", ");
    this.images.forEach((image) => this.tagImage(image, tags));
  }

  tagImage(image: Image, tags: string): void {
    const oldExifObj = piexif.load(image.content);
    oldExifObj["0th"][piexif.ImageIFD.ImageDescription] = tags;
    oldExifObj["Exif"][piexif.ExifIFD.UserComment] = tags;
    const exifbytes = piexif.dump(oldExifObj);
    const exifObj = piexif.insert(exifbytes, image.content);
    download(exifObj, image.name, image.type);
  }
}

interface Item {
  id: string;
  name: string;
  children?: Item[];
}

class Image {
  public name: string;
  public type: string;
  constructor(file: File, public content: string) {
    this.name = file.name;
    this.type = file.type;
  }
}
</script>
