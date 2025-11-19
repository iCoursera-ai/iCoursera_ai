const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    port: 8080,
    open: true,
    proxy: {
      '/api': {
        target: 'http://localhost:3000',
        changeOrigin: true,
        pathRewrite: {
          '^/api': ''
        }
      }
    }
  },
  configureWebpack: {
    resolve: {
      alias: {
        '@': require('path').resolve(__dirname, 'src')
      }
    }
  },
  css: {
    loaderOptions: {
      css: {
        modules: {
          auto: true
        }
      }
    }
  },
  // 生产环境配置
  publicPath: process.env.NODE_ENV === 'production' ? '/edulearn/' : '/',
  outputDir: 'dist',
  assetsDir: 'static',
  productionSourceMap: false
})