<template>
  <v-card>
    <v-card-title>
      <v-text-field
        v-if="model"
        v-model="model.name"
        :rules="[rules.required]"
        label="Filename"
      ></v-text-field>
    </v-card-title>
    <v-card-text>
      <v-img :src="model?.content" contain max-height="256">
        <template #placeholder>
          <v-row class="fill-height ma-0" align="center" justify="center">
            <v-progress-circular
              indeterminate
              color="primary"
            ></v-progress-circular>
          </v-row>
        </template>
      </v-img>
      <div v-if="model !== undefined">
        <h1>Author</h1>
        <div>
          <span
            v-if="model.authorChanged"
            class="red--text text-decoration-line-through"
          >
            {{ model.oldAuthor }}
          </span>
          <span :class="{ 'green--text': model.authorChanged }">{{
            model.newAuthor
          }}</span>
        </div>
        <br />
        <h1>License</h1>
        <div>
          <span
            v-if="model.copyrightChanged"
            class="red--text text-decoration-line-through"
          >
            {{ model.oldCopyright }}
          </span>
          <span :class="{ 'green--text': model.authorChanged }">
            {{ model.newCopyright }}
          </span>
        </div>
        <br />
        <h1>Tags</h1>
        <v-chip-group column>
          <v-chip
            v-for="(tag, j) in model.removedTags"
            :key="j"
            color="red"
            dark
            small
            close
            close-icon="mdi-plus-circle"
            @click:close="onCloseAddTag(tag)"
          >
            <span class="text-decoration-line-through">
              {{ tag }}
            </span>
          </v-chip>
        </v-chip-group>
        <v-chip-group column>
          <v-chip
            v-for="(tag, j) in model.unmodifiedTags"
            :key="j"
            color="grey"
            dark
            small
            close
            close-icon="mdi-minus-circle"
            @click:close="onCloseRemoveTag(tag)"
          >
            {{ tag }}
          </v-chip>
          <v-chip
            v-for="(tag, j) in model.addedTags"
            :key="model.unmodifiedTags.length + j"
            color="green"
            dark
            small
            close
            close-icon="mdi-minus-circle"
            @click:close="onCloseRemoveTag(tag)"
          >
            {{ tag }}
          </v-chip>
        </v-chip-group>
        <v-expansion-panels>
          <v-expansion-panel>
            <v-expansion-panel-header>Metadata</v-expansion-panel-header>
            <v-expansion-panel-content>
              <pre>{{ model.metadata }}</pre>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </div>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import UploadImage from "@/models/upload-image";
import rules from "@/utils/rules";
import Vue from "vue";
import Component from "vue-class-component";
import { VModel } from "vue-property-decorator";

@Component
export default class ImageItem extends Vue {
  readonly rules = rules;
  @VModel()
  model!: UploadImage;

  onCloseAddTag(tag: string): void {
    this.model.addTag(tag);
    this.notify();
  }

  onCloseRemoveTag(tag: string): void {
    this.model.removeTag(tag);
    this.notify();
  }

  private notify(): void {
    const image: UploadImage = Object.assign(
      new UploadImage(this.model.name, this.model.type, this.model.content),
      this.model
    );
    this.$emit("input", image);
  }
}
</script>
