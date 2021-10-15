<template>
  <v-row>
    <v-col cols="8">
      <composition-editor :images="images"></composition-editor>
    </v-col>
    <v-col cols="4">
      <image-browser @add="addImage"></image-browser>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";
import ImageBrowser from "@/components/ImageBrowser.vue";
import BackendImage from "@/models/backend-image";
import CompositionEditor from "@/components/CompositionEditor.vue";
import { ComposedImage } from "@/backend";

@Component({
  components: {
    CompositionEditor,
    ImageBrowser,
  },
})
export default class Workspace extends Vue {
  images: ComposedImage[] = [];

  addImage(image: BackendImage): void {
    const maxInitSize = 200;
    const ratio = Math.max(image.width, image.height) / maxInitSize;
    this.images.push({
      id: image.id,
      url: image.url,
      x: 0,
      y: 0,
      width: image.width / ratio,
      height: image.height / ratio,
    });
  }
}
</script>
