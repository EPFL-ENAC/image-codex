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
import { TaggedImage } from "@/backend";
import CompositionEditor from "@/components/CompositionEditor.vue";
import ImageBrowser from "@/components/ImageBrowser.vue";
import Vue from "vue";
import Component from "vue-class-component";

@Component({
  components: {
    CompositionEditor,
    ImageBrowser,
  },
})
export default class Workspace extends Vue {
  addImage(image: TaggedImage): void {
    const editor = this.$refs.editor as CompositionEditor;
    editor.addImage(image);
  }
}
</script>
