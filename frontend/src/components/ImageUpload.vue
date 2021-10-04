<template>
  <v-card flat>
    <v-card-title>Image Metadata Editor</v-card-title>
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
            <v-form v-model="formValid">
              <v-row>
                <v-text-field
                  v-model="author"
                  label="Author"
                  :rules="[rules.required]"
                  required
                  @change="onChangeAuthor"
                ></v-text-field>
              </v-row>
              <v-row>
                <v-select
                  v-model="license"
                  :items="licenses"
                  :rules="[rules.required]"
                  label="License"
                  required
                >
                  <template v-slot:append-outer>
                    <v-btn
                      icon
                      href="https://creativecommons.org/choose/"
                      target="_blank"
                    >
                      <v-icon>mdi-information</v-icon>
                    </v-btn>
                  </template>
                </v-select>
              </v-row>
              <v-row>
                <v-combobox
                  v-model="selectedTags"
                  label="Tags"
                  chips
                  deletable-chips
                  multiple
                ></v-combobox>
              </v-row>
              <v-row>
                <v-text-field
                  v-model="search"
                  label="Search Categories"
                  hide-details
                  clearable
                ></v-text-field>
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
                  :disabled="!formValid || images.length == 0"
                  @click="onClickAddToImage"
                >
                  <v-icon left>mdi-plus-circle</v-icon>
                  Add to images
                </v-btn>
              </v-row>
            </v-form>
          </v-sheet>
        </v-col>
      </v-row>
    </v-card-text>
    <v-card-actions>
      <v-btn
        :disabled="!isValidImages"
        :loading="imagesUploading"
        color="primary"
        @click="onUploadImages"
      >
        <v-icon left>mdi-cloud-upload</v-icon>
        Upload Images
      </v-btn>
      <v-btn
        :disabled="!isValidImages"
        color="primary"
        @click="onDownloadImages"
      >
        <v-icon left>mdi-download</v-icon>
        Download Images
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";
import download from "downloadjs";
import categories from "@/assets/categories.yaml";
import ImageItem from "./ImageItem.vue";
import UploadImage from "@/models/upload-image";
import rules from "@/utils/rules";
import { LocalStorageKey, tagSeparator } from "@/utils/contants";
import { unique } from "@/utils/functions";

@Component({
  components: {
    ImageItem,
  },
})
export default class ImageUpload extends Vue {
  readonly rules = rules;
  readonly licenses = [
    "Creative Commons Attribution 4.0 International License",
  ];

  formValid = false;
  author = localStorage.getItem(LocalStorageKey.Author) ?? "";
  license = this.licenses[0];
  search = "";
  selectedCategories: string[] = [];
  customTags: string[] = [];
  imageFiles: File[] = [];
  images: UploadImage[] = [];
  imagesUploading = false;

  get treeCategories(): Item[] {
    return this.parseTree(categories);
  }

  get selectedTags(): string[] {
    return this.selectedCategories
      .flatMap((categories) => categories.split(tagSeparator))
      .filter(unique)
      .concat(this.customTags)
      .sort();
  }

  set selectedTags(values: string[]) {
    const tags = new Set(values);
    this.selectedCategories = this.selectedCategories.filter((category) =>
      category.split(tagSeparator).every((tag) => tags.has(tag))
    );
    const categories = new Set(
      this.selectedCategories.flatMap((categories) =>
        categories.split(tagSeparator)
      )
    );
    this.customTags = values.filter((value) => !categories.has(value));
  }

  get treeArray(): unknown[] {
    return this.parseTreeArray(categories).map((item) => {
      return {
        text: item[item.length - 1],
        value: item,
      };
    });
  }

  get isValidImages(): boolean {
    return (
      this.images.length > 0 && this.images.every((image) => image.isValid)
    );
  }

  parseTree(obj: unknown, parents: string[] = []): Item[] {
    return Object.entries(obj as Record<string, unknown>).flatMap(
      ([key, value]) => {
        const id = [...parents, key];
        const type = typeof value;
        if (type === "object") {
          if (value === null) {
            return [
              {
                id: id.join(tagSeparator),
                name: key,
              },
            ];
          } else {
            return [
              {
                id: id.join(tagSeparator),
                name: key,
                children: this.parseTree(value, id),
              },
            ];
          }
        } else {
          console.error(`unexpected type ${type} for key ${id.join(".")}`);
          return [];
        }
      }
    );
  }

  parseTreeArray(obj: unknown, parents: string[] = []): string[][] {
    return Object.entries(obj as Record<string, unknown>).flatMap(
      ([key, value]) => {
        const id = [...parents, key];
        const type = typeof value;
        if (type === "object") {
          if (value === null) {
            return [id];
          } else {
            return this.parseTreeArray(value, id);
          }
        } else {
          console.error(`unexpected type ${type} for key ${id.join(".")}`);
          return [];
        }
      }
    );
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
        (content, i) => new UploadImage(files[i], content)
      ));
    });
  }

  onChangeAuthor(): void {
    localStorage.setItem(LocalStorageKey.Author, this.author);
  }

  onDownloadImages(): void {
    this.images.forEach((image) => {
      const content = image.write();
      download(content, image.name, image.type);
    });
  }

  onUploadImages(): void {
    this.imagesUploading = true;
    Promise.all(
      this.images.map((image) => {
        const content = image.write();
        const data = content.startsWith("data:")
          ? content?.split(",")[1]
          : content;
        return this.$http.post("/images", { content: data });
      })
    ).then(() => {
      this.imagesUploading = false;
    });
  }

  onClickAddToImage(): void {
    const tags = this.selectedTags;
    this.images.forEach((image) => {
      image.newAuthor = this.author;
      image.newCopyright = this.license;
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
