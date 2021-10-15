<template>
  <v-row>
    <v-col cols="8">
      <composition-editor ref="editor"></composition-editor>
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
import CompositionEditor from "@/components/CompositionEditor.vue";
import { ResponseImage } from "@/backend";

@Component({
  components: {
    CompositionEditor,
    ImageBrowser,
  },
})
export default class Workspace extends Vue {
  addImage(image: ResponseImage): void {
    const editor = this.$refs.editor as CompositionEditor;
    editor.addImage(image);
  }
}
</script>
