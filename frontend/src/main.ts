import Vue from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";
import vuetify from "./plugins/vuetify";
import axios from "axios";
import i18n from "./i18n";
import store from "./store";

Vue.config.productionTip = false;

Vue.prototype.$http = axios.create({
  baseURL: process.env.VUE_APP_BACKEND_URL,
});

new Vue({
  router,
  vuetify,
  i18n,
  store,
  render: (h) => h(App),
}).$mount("#app");
