import "./registerServiceWorker";
import "vue-draggable-resizable/dist/VueDraggableResizable.css";

import App from "./App.vue";
import Vue from "vue";
import VueDraggableResizable from "vue-draggable-resizable";
import axios from "axios";
import i18n from "./i18n";
import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";

Vue.config.productionTip = false;

Vue.prototype.$http = axios.create({
  baseURL: process.env.VUE_APP_BACKEND_URL,
});

Vue.component("vue-draggable-resizable", VueDraggableResizable);

new Vue({
  router,
  vuetify,
  i18n,
  store,
  render: (h) => h(App),
}).$mount("#app");
