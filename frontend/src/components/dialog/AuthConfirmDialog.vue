<template>
  <v-dialog v-model="dialog" max-width="256">
    <v-card>
      <v-form v-model="valid">
        <v-card-title>
          {{ title }}
        </v-card-title>
        <v-card-text>
          {{ message }}
          <v-text-field
            v-model="username"
            label="Username"
            :rules="[rules.required]"
            type="text"
            required
          ></v-text-field>
          <v-text-field
            v-model="password"
            label="Password"
            :rules="[rules.required]"
            type="password"
            required
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" :disabled="!valid" text @click="confirm">
            Confirm
          </v-btn>
          <v-btn text @click="cancel"> Cancel </v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import rules from "@/utils/rules";
import { AxiosBasicCredentials } from "axios";
import Vue from "vue";
import Component from "vue-class-component";

@Component
export default class AuthConfirmDialog extends Vue {
  readonly rules = rules;
  dialog = false;
  valid = true;
  title = "";
  message = "";
  username = "";
  password = "";
  resolve: (
    value: AxiosBasicCredentials | PromiseLike<AxiosBasicCredentials>
  ) => void = () => null;

  open(
    message: string,
    title = "Confirmation"
  ): Promise<AxiosBasicCredentials> {
    this.title = title;
    this.message = message;
    this.dialog = true;
    return new Promise((resolve) => {
      this.resolve = resolve;
    });
  }

  confirm(): void {
    const credential: AxiosBasicCredentials = {
      username: this.username,
      password: this.password,
    };
    this.resolve(credential);
    this.dialog = false;
  }

  cancel(): void {
    this.dialog = false;
  }
}
</script>
