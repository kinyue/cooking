// frontend/src/plugins/vuetify.js
// Vuetify 3 plugin configuration

import 'vuetify/styles' // Import Vuetify styles
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// Optional: Import Material Design Icons
import '@mdi/font/css/materialdesignicons.css' // Ensure you have installed `@mdi/font`

const vuetify = createVuetify({
  components,
  directives,
  // Optional: Define a custom theme
  // theme: {
  //   defaultTheme: 'light', // or 'dark'
  //   themes: {
  //     light: {
  //       dark: false,
  //       colors: {
  //         primary: '#1976D2', // Example primary color
  //         secondary: '#424242',
  //         accent: '#82B1FF',
  //         error: '#FF5252',
  //         info: '#2196F3',
  //         success: '#4CAF50',
  //         warning: '#FB8C00',
  //       }
  //     },
      // dark: { ... } // Define dark theme colors if needed
  //   }
  // },
  // Optional: Set default icons
  // icons: {
  //   defaultSet: 'mdi', // Use Material Design Icons
  // },
})

export default vuetify
