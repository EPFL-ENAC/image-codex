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
        clearable
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
                :color="getTagColor(tag)"
                :key="tag"
                small
              >
                {{ tag }}
              </v-chip>
            </v-chip-group>
            <v-card-actions>
              <v-btn color="primary" icon @click="$emit('add', item)">
                <v-icon>mdi-plus</v-icon>
              </v-btn>
              <v-btn icon @click="deleteImage(item.id)">
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
    <confirm-dialog ref="confirmDialog"></confirm-dialog>
  </v-card>
</template>

<style scoped>
.scrollable {
  overflow-y: scroll;
}
</style>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import { paramsSerializer } from "@/utils/functions";
import TagSelector from "./TagSelector.vue";
import ConfirmDialog from "./ConfirmDialog.vue";
import { CursorPageTaggedImage, TaggedImage } from "@/backend";

@Component({
  components: {
    ConfirmDialog,
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
    this.$http
      .get<CursorPageTaggedImage>("/images", {
        params: {
          size: this.pageSize,
          next: this.next,
          tags: this.selectedTags,
          author: this.author ? this.author : undefined,
        },
        paramsSerializer: paramsSerializer,
      })
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

  deleteImage(id: string): void {
    const confirmDialog: ConfirmDialog = this.$refs
      .confirmDialog as ConfirmDialog;
    confirmDialog.open(`image ${id} will be deleted`).then((confirmed) => {
      if (confirmed) {
        this.$http.delete(`/images/${id}`).then(() => this.initializeImages());
      }
    });
  }
}
</script>
