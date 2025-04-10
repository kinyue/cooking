const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
  chainWebpack: config => {
    // Define Vue feature flags
    config.plugin('define').tap(definitions => {
      Object.assign(definitions[0], {
        // Enable/disable features. Recommended defaults for Vue 3.
        __VUE_OPTIONS_API__: JSON.stringify(true), // Keep Options API support
        __VUE_PROD_DEVTOOLS__: JSON.stringify(false), // Disable devtools in production
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: JSON.stringify(false) // Disable detailed hydration mismatch warnings in production
      });
      return definitions;
    });
  }
});
