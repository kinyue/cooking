// frontend/src/plugins/vuetify.js
// Vuetify 3 plugin configuration

import 'vuetify/styles' // Import Vuetify styles
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// Optional: Import Material Design Icons
import '@mdi/font/css/materialdesignicons.css' // Ensure you have installed `@mdi/font`

// Define the custom light theme
const myCustomLightTheme = {
  dark: false,
  colors: {
    background: '#F5F5F5', // Light grey background for the page
    surface: '#FFFFFF',    // White background for components like cards, app-bar
    primary: '#4CAF50',    // Green color for the primary button ('开始推荐')
    'primary-darken-1': '#388E3C',
    secondary: '#607D8B',  // A secondary color (adjust as needed)
    'secondary-darken-1': '#455A64',
    error: '#FF5252',
    info: '#2196F3',
    success: '#4CAF50',    // Can be the same as primary or different green
    warning: '#FB8C00',
    // Define text colors if needed, often inferred correctly
    // 'on-background': '#333333',
    // 'on-surface': '#333333',
    // 'on-primary': '#FFFFFF',
  },
}

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'myCustomLightTheme', // Set the custom theme as default
    themes: {
      myCustomLightTheme, // Register the custom theme
      // You could also define a dark theme here if needed
    },
  },
  icons: {
    defaultSet: 'mdi', // Use Material Design Icons
  },
})

export default vuetify