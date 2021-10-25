<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-app-bar-title>Image Codex</v-app-bar-title>
      <v-spacer></v-spacer>
      <v-dialog v-model="usernameDialog" max-width="256" persistent>
        <template v-slot:activator="{ on, attrs }">
          <v-btn v-bind="attrs" v-on="on" text>
            {{ username }}
          </v-btn>
        </template>
        <v-card>
          <v-form @submit.prevent="usernameDialog = false">
            <v-card-title>Username</v-card-title>
            <v-card-text>
              <v-text-field v-model="username"></v-text-field>
            </v-card-text>
            <v-card-actions>
              <v-btn color="primary" :disabled="!username" type="submit" text>
                Ok
              </v-btn>
            </v-card-actions>
          </v-form>
        </v-card>
      </v-dialog>
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
  usernameDialog = !this.username;

  get username(): string {
    return this.$store.state.username;
  }

  set username(value: string) {
    this.$store.commit("setUsername", value);
  }

  setLanguage(language: string): void {
    this.$i18n.locale = language;
    localStorage.setItem(LocalStorageKey.Language, language);
  }
}
</script>
