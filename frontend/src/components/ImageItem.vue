<template>
  <v-card>
    <v-card-title>
      <v-text-field
        v-if="value"
        v-model="value.name"
        :rules="[rules.required]"
        label="Filename"
      ></v-text-field>
    </v-card-title>
    <v-card-text>
      <v-img :src="value?.content" contain max-height="256">
        <template v-slot:placeholder>
          <v-row class="fill-height ma-0" align="center" justify="center">
            <v-progress-circular
              indeterminate
              color="primary"
            ></v-progress-circular>
          </v-row>
        </template>
      </v-img>
      <div v-if="value !== undefined">
        <h1>Author</h1>
        <div>
          <span
            v-if="value.authorChanged"
            class="red--text text-decoration-line-through"
          >
            {{ value.oldAuthor }}
          </span>
          <span :class="{ 'green--text': value.authorChanged }">{{
            value.newAuthor
          }}</span>
        </div>
        <br />
        <h1>License</h1>
        <div>
          <span
            v-if="value.copyrightChanged"
            class="red--text text-decoration-line-through"
          >
            {{ value.oldCopyright }}
          </span>
          <span :class="{ 'green--text': value.authorChanged }">
            {{ value.newCopyright }}
          </span>
        </div>
        <br />
        <h1>Tags</h1>
        <v-chip-group column>
          <v-chip
            v-for="(tag, j) in value.removedTags"
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
            v-for="(tag, j) in value.unmodifiedTags"
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
            v-for="(tag, j) in value.addedTags"
            :key="value.unmodifiedTags.length + j"
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
              <pre>{{ value.metadata }}</pre>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </div>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";
import Image from "@/models/image";
import rules from "@/utils/rules";

const ImageItemProps = Vue.extend({
  props: {
    value: Image,
  },
});

@Component
export default class ImageItem extends ImageItemProps {
  readonly rules = rules;

  onCloseAddTag(tag: string): void {
    this.value.addTag(tag);
    this.notify();
  }

  onCloseRemoveTag(tag: string): void {
    this.value.removeTag(tag);
    this.notify();
  }

  private notify(): void {
    const image: Image = Object.assign(new Image(), this.value);
    this.$emit("input", image);
  }
}
</script>
