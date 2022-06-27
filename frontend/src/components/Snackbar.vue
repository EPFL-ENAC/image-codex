<template>
  <v-snackbar v-model="snackbar">
    {{ message }}
    <template #action="{ attrs }">
      <v-btn v-bind="attrs" color="primary" icon @click="snackbar = false">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";

@Component
export default class Snackbar extends Vue {
  snackbar = false;
  message = "";

  open(message: string): void {
    this.message = message;
    this.snackbar = true;
  }
}
</script>
