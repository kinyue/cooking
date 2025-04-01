<template>
  <v-app>
    <app-header />
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
import AppHeader from '@/components/AppHeader.vue';
</script>

<style scoped>
/* Optional: Scoped styles for App.vue */
.v-main {
  /* Use the background color from the theme */
  background-color: rgb(var(--v-theme-background));
  padding-top: 64px; /* Adjust based on AppHeader height if needed */
}
</style>
