module.exports = {
  chainWebpack: (config) => {
    config.module
      .rule("vue")
      .use("vue-loader")
      .tap((options) => {
        options.compiler = require("vue-template-babel-compiler");
        return options;
      });
    config.module
      .rule("yaml")
      .test(/\.ya?ml$/)
      .type("json")
      .use("yaml-loader")
      .options({ asJSON: true })
      .loader("yaml-loader")
      .end();
  },

  transpileDependencies: ["vuetify"],

  pluginOptions: {
    i18n: {
      locale: "en",
      fallbackLocale: "en",
      localeDir: "locales",
      enableInSFC: false,
      enableBridge: false,
    },
  },
};
