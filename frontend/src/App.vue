<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Image Codex</v-toolbar-title>
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

export default Vue.extend({
  name: "App",

  data: () => ({
    //
  }),
});
</script>
