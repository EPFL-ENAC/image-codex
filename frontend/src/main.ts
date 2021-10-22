import "./registerServiceWorker";
import "leaflet/dist/leaflet.css";
import "vue-draggable-resizable/dist/VueDraggableResizable.css";

import App from "./App.vue";
import { Icon } from "leaflet";
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

// https://vue2-leaflet.netlify.app/quickstart/#marker-icons-are-missing
type D = Icon.Default & {
  _getIconUrl?: string;
};
delete (Icon.Default.prototype as D)._getIconUrl;
Icon.Default.mergeOptions({
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  shadowUrl: require("leaflet/dist/images/marker-shadow.png"),
});
