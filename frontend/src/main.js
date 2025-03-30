// frontend/src/main.js
// Main entry point for the Vue application

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify' // Import Vuetify plugin
// import { createPinia } from 'pinia' // Uncomment if using Pinia

import './assets/main.css' // Optional: main CSS file

const app = createApp(App)

// Use plugins
app.use(router)
app.use(vuetify)
// app.use(createPinia()) // Uncomment if using Pinia

app.mount('#app')
