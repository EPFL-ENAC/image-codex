<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Image Codex</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-menu>
        <template v-slot:activator="{ on, attrs }">
          <v-btn v-bind="attrs" v-on="on" text>
            {{ $i18n.locale }}
          </v-btn>
        </template>
        <v-list>
          <v-list-item
            v-for="language in languages"
            :key="language"
            @click="setLanguage(language)"
          >
            <v-list-item-title>{{ language }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
      <!-- <v-select
        v-model="$i18n.locale"
        hide-details
        :items="languages"
      ></v-select> -->
      <template v-slot:extension>
        <v-tabs>
          <v-tab to="/">Home</v-tab>
          <v-tab to="/upload">Upload</v-tab>
          <v-tab to="/workspace">Workspace</v-tab>
          <v-tab to="/about">About</v-tab>
        </v-tabs>
      </template>
    </v-app-bar>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";
import { LocalStorageKey } from "./utils/contants";

@Component
export default class App extends Vue {
  languages = ["en", "de"];

  setLanguage(language: string): void {
    this.$i18n.locale = language;
    localStorage.setItem(LocalStorageKey.Language, language);
  }
}
</script>
