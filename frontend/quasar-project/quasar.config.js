import { defineConfig } from '#q-app/wrappers'

export default defineConfig((ctx) => {
  // 환경 정보 출력
  console.log(`🔧 Mode: ${ctx.mode}`)
  console.log(`🔧 API URL: ${process.env.VITE_API_URL}`)
  console.log(`🔧 App Title: ${process.env.VITE_APP_TITLE}`)
  console.log(`🔧 Debug: ${process.env.VITE_DEBUG}`)
  
  return {
    boot: [
      'pinia'
    ],
    plugins: [
      'Notify'
    ],
    css: ['app.scss'],
    
    extras: [
      'roboto-font',
      'material-icons',
    ],

    build: {
      target: {
        browser: [ 'es2022', 'firefox115', 'chrome115', 'safari14' ],
        node: 'node20'
      },
      vueRouterMode: 'hash',
      vitePlugins: [
        ['vite-plugin-checker', {
          eslint: {
            lintCommand: 'eslint -c ./eslint.config.js "./src*/**/*.{js,mjs,cjs,vue}"',
            useFlatConfig: true
          }
        }, { server: false }]
      ]
    },

    devServer: {
      open: true,
      port: 9000
    },

    framework: {
      config: {},
      plugins: ['Notify']
    },

    animations: [],
    
    ssr: {
      prodPort: 3000,
      middlewares: ['render'],
      pwa: false
    },

    pwa: {
      workboxMode: 'GenerateSW'
    },

    cordova: {},
    capacitor: {
      hideSplashscreen: true
    },

    electron: {
      preloadScripts: [ 'electron-preload' ],
      inspectPort: 5858,
      bundler: 'packager',
      packager: {},
      builder: {
        appId: 'quasar-project'
      }
    },

    bex: {
      extraScripts: []
    }
  }
})
