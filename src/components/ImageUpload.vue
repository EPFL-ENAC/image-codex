<template>
  <v-card flat>
    <v-card-title>Image Tagging</v-card-title>
    <v-card-text>
      <v-row>
        <v-col cols="8">
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
          <v-row>
            <v-col v-for="(file, i) in imageFiles" :key="i">
              <v-card>
                <v-img
                  :src="images[i]?.content"
                  :lazy-src="file.name"
                  contain
                  max-height="256"
                >
                  <template v-slot:placeholder>
                    <v-row
                      class="fill-height ma-0"
                      align="center"
                      justify="center"
                    >
                      <v-progress-circular
                        indeterminate
                        color="primary"
                      ></v-progress-circular>
                    </v-row> </template
                ></v-img>
                <div v-if="images[i]">
                  <v-chip-group column>
                    <v-chip
                      v-for="(tag, i) in images[i].originalTags"
                      :key="i"
                      small
                    >
                      {{ tag }}
                    </v-chip>
                  </v-chip-group>
                </div>
              </v-card>
            </v-col>
          </v-row>
        </v-col>
        <v-col cols="4">
          <v-text-field
            v-model="search"
            label="Search Categories"
            hide-details
            clearable
          ></v-text-field>
          <v-row class="ma-1" align="center">
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
            <v-btn
              v-if="selectedCategories.length > 0"
              icon
              @click="selectedCategories = []"
            >
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-row>
          <v-treeview
            v-model="selectedCategories"
            :items="treeCategories"
            :search="search"
            open-on-click
            selectable
            selection-type="independent"
          ></v-treeview>
        </v-col>
      </v-row>
    </v-card-text>
    <v-card-actions>
      <v-btn
        :disabled="imageFiles.length == 0 || selectedCategories.length == 0"
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
import piexif from "piexifjs";
import categories from "../assets/categories.yaml";

@Component
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
    const tags = this.selectedTags.join(this.tagSeparator);
    this.images.forEach((image) => this.tagImage(image, tags));
  }

  onCloseTag(tag: string): void {
    this.selectedCategories = this.selectedCategories.filter((category) => {
      return !category.split(this.tagSeparator).some((t) => t === tag);
    });
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
  static readonly attributes: string[][] = [
    ["0th", piexif.ImageIFD.ImageDescription],
    ["Exif", piexif.ExifIFD.UserComment],
  ];

  public name: string;
  public type: string;
  private originalTagsSet: Set<string>;

  private exif: Record<string, Record<string, string>>;

  constructor(file: File, public content: string) {
    this.name = file.name;
    this.type = file.type;
    this.exif = piexif.load(content);
    this.originalTagsSet = Image.getTags(this.exif);
  }

  static getTags(exif: Record<string, Record<string, string>>): Set<string> {
    return new Set(
      Image.attributes
        .map((attribute) => exif[attribute[0]][attribute[1]])
        .filter((tags) => tags !== undefined)
        .map((tags) => tags.replace(/ASCII|[^\x20-\x7E]/g, ""))
        .flatMap((tags) => tags.split(","))
        .map((tag) => tag.trim())
        .filter((tag) => tag.length > 0)
        .map((tag) => tag.toLowerCase())
    );
  }

  get originalTags(): string[] {
    return Array.from(this.originalTagsSet).sort();
  }
}
</script>
