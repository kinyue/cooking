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
@import '@/assets/app.css';
</style>
