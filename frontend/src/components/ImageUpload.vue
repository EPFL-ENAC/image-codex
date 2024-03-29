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
              <v-row v-if="licenses.length > 1">
                <v-select
                  v-model="license"
                  :items="licenses"
                  :rules="[rules.required]"
                  label="License"
                  required
                >
                  <template #append-outer>
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
                <tag-selector v-model="tags"></tag-selector>
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
import { ApiFile } from "@/backend";
import TagSelector from "@/components/TagSelector.vue";
import UploadImage from "@/models/upload-image";
import { mapDataUrlToBase64 } from "@/utils/functions";
import rules from "@/utils/rules";
import download from "downloadjs";
import { extension } from "mime-types";
import { Component, Vue } from "vue-property-decorator";
import ImageItem from "./ImageItem.vue";

@Component({
  components: {
    ImageItem,
    TagSelector,
  },
})
export default class ImageUpload extends Vue {
  readonly rules = rules;
  readonly licenses = [
    "Creative Commons Attribution 4.0 International License",
  ];

  formValid = false;
  license = this.licenses[0];
  search = "";
  imageFiles: File[] = [];
  images: UploadImage[] = [];
  tags: string[] = [];
  imagesUploading = false;

  get isValidImages(): boolean {
    return (
      this.images.length > 0 && this.images.every((image) => image.isValid)
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
      this.images = contents.map((content, i) => {
        const file = files[i];
        return new UploadImage(file.name, file.type, content);
      });
      this.images.forEach((image) => {
        const apiFile: ApiFile = {
          type: image.type,
          base64: mapDataUrlToBase64(image.content),
        };
        this.$hashApi
          .getImageHashHashImagePost(apiFile)
          .then((response) => response.data)
          .then((hash) => {
            const ext: string = extension(image.type) || "";
            image.name = `${hash}.${ext}`;
          });
      });
    });
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
        const apiFile: ApiFile = {
          name: image.name,
          type: image.type,
          base64: mapDataUrlToBase64(content),
        };
        return this.$imagesApi.createImageImagesPost(apiFile);
      })
    )
      .catch((reason) => {
        console.error(reason);
      })
      .finally(() => {
        this.imagesUploading = false;
      });
  }

  onClickAddToImage(): void {
    const tags = this.tags;
    this.images = this.images.map((image) => {
      image.newAuthor = this.$store.state.username;
      image.newCopyright = this.license;
      image.addTags(tags);
      return image;
    });
    const imageItems: Vue[] = this.$refs.imageItems as Vue[];
    imageItems.forEach((item) => {
      item.$forceUpdate();
    });
  }
}
</script>
