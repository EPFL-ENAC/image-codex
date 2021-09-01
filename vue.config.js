module.exports = {
  chainWebpack: (config) => {
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
};
