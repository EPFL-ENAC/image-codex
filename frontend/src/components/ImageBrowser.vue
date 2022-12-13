<template>
  <v-card height="90vh" class="scrollable">
    <v-card-text>
      <tag-selector
        v-model="selectedTags"
        @change="initializeImages"
      ></tag-selector>
      <v-text-field
        v-model="author"
        label="Author"
        @change="initializeImages"
      ></v-text-field>
      <v-row>
        <v-col v-if="images.length === 0">
          <span>No images</span>
        </v-col>
        <v-col v-for="item in images" :key="item.id" cols="12" sm="12" md="6">
          <v-card>
            <v-img :src="item.url"></v-img>
            <v-chip-group class="mx-2" column>
              <v-chip
                v-for="tag in item.tags"
                :key="tag"
                :color="getTagColor(tag)"
                small
              >
                {{ tag }}
              </v-chip>
            </v-chip-group>
            <v-card-actions>
              <v-btn
                color="primary"
                title="Add to composition"
                icon
                @click="$emit('add', item)"
              >
                <v-icon>mdi-plus</v-icon>
              </v-btn>
              <v-btn icon title="Edit" @click="editImage(item)">
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
              <v-btn icon title="Delete" @click="deleteImage(item.id)">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
        <v-col v-if="next">
          <v-badge color="secondary" :content="remainingImagesCount" overlap>
            <v-btn color="primary" fab small @click="getNextImages">
              <v-icon>mdi-dots-horizontal</v-icon>
            </v-btn>
          </v-badge>
        </v-col>
      </v-row>
    </v-card-text>
    <image-editor-dialog ref="editDialog"></image-editor-dialog>
    <auth-confirm-dialog ref="editConfirmDialog"></auth-confirm-dialog>
    <auth-confirm-dialog ref="deleteConfirmDialog"></auth-confirm-dialog>
  </v-card>
</template>

<script lang="ts">
import { TaggedImage } from "@/backend";
import { AxiosError } from "axios";
import { Component, Vue } from "vue-property-decorator";
import AuthConfirmDialog from "./dialog/AuthConfirmDialog.vue";
import ImageEditorDialog from "./dialog/ImageEditorDialog.vue";
import TagSelector from "./TagSelector.vue";

@Component({
  components: {
    AuthConfirmDialog,
    ImageEditorDialog,
    TagSelector,
  },
})
export default class ImageBrowser extends Vue {
  selectedTags: string[] = [];
  images: TaggedImage[] = [];
  readonly pageSize = 4;
  next: string | undefined = undefined;
  imagesCount = 0;
  author = this.$store.state.username;

  get remainingImagesCount(): number {
    return this.imagesCount - this.images.length;
  }

  created(): void {
    this.initializeImages();
  }

  getTagColor(tag: string): string | undefined {
    return this.selectedTags.includes(tag) ? "secondary" : undefined;
  }

  private updateItems(callback: (images: TaggedImage[]) => void) {
    this.$imagesApi
      .getAllImagesImagesGet(
        this.selectedTags,
        this.author ? this.author : undefined,
        this.next,
        this.pageSize
      )
      .then((response) => {
        this.next = response.data.next;
        this.imagesCount = response.data.total;
        callback(response.data.items);
      });
  }

  initializeImages(): void {
    this.next = undefined;
    this.images = [];
    this.getNextImages();
  }

  getNextImages(): void {
    this.updateItems((images) => this.images.push(...images));
  }

  editImage(image: TaggedImage): void {
    const dialog: ImageEditorDialog = this.$refs
      .editDialog as ImageEditorDialog;
    const confirmDialog: AuthConfirmDialog = this.$refs
      .editConfirmDialog as AuthConfirmDialog;
    dialog
      .open(image)
      .then((image) =>
        confirmDialog
          .open(`Image ${image.id} will be modified on the server.`)
          .then((credential) =>
            this.$imagesApi.updateImageImagesImageIdPost(image.id, image, {
              auth: credential,
            })
          )
      )
      .then(() => new Promise((f) => setTimeout(f, 1000)))
      .then(() => this.initializeImages())
      .catch(this.onApiError);
  }

  deleteImage(id: string): void {
    const dialog: AuthConfirmDialog = this.$refs
      .deleteConfirmDialog as AuthConfirmDialog;
    dialog
      .open(`Image ${id} will be permanently deleted from the server.`)
      .then((credential) =>
        this.$imagesApi.deleteImagesImagesImageIdsDelete(id, {
          auth: credential,
        })
      )
      .then(() => this.initializeImages())
      .catch(this.onApiError);
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  onApiError(error: AxiosError<any>): void {
    this.$store.commit("setSnackbar", error.response?.data.detail ?? error);
  }
}
</script>

<style scoped>
.scrollable {
  overflow-y: auto;
}
</style>
