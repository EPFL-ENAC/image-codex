import { LocalStorageKey } from "@/utils/contants";
import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    snackbar: "",
    username: localStorage.getItem(LocalStorageKey.Username) ?? "",
  },
  mutations: {
    setSnackbar(state, message: string) {
      state.snackbar = message;
    },
    setUsername(state, username: string) {
      state.username = username;
      localStorage.setItem(LocalStorageKey.Username, username);
    },
  },
  actions: {},
  modules: {},
});
