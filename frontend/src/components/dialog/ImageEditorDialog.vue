<template>
  <v-dialog v-model="dialog" max-width="512" @click:outside="cancel">
    <v-card v-if="image">
      <v-card-title>
        {{ image.id }}
      </v-card-title>
      <v-card-text>
        <v-img :src="image.url"></v-img>
        <tag-selector v-model="image.tags"></tag-selector>
      </v-card-text>
      <v-card-actions>
        <v-btn
          color="primary"
          :disabled="image.tags.length === 0"
          text
          @click="confirm"
        >
          Save
        </v-btn>
        <v-btn text @click="cancel"> Cancel </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import { TaggedImage } from "@/backend";
import TagSelector from "@/components/TagSelector.vue";

@Component({
  components: {
    TagSelector,
  },
})
export default class ImageEditorDialog extends Vue {
  dialog = false;
  image: TaggedImage | null = null;
  resolve: (value: TaggedImage | PromiseLike<TaggedImage>) => void = () => null;

  open(image: TaggedImage): Promise<TaggedImage> {
    this.image = Object.assign({}, image);
    this.dialog = true;
    return new Promise((resolve) => {
      this.resolve = resolve;
    });
  }

  confirm(): void {
    if (this.image) {
      this.resolve(this.image);
      this.dialog = false;
    }
  }

  cancel(): void {
    this.image = null;
    this.dialog = false;
  }

  removeTag(tag: string): void {
    if (this.image) {
      this.image.tags = this.image.tags.filter((t) => t !== tag);
    }
  }
}
</script>
