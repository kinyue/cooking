<template>
  <v-app-bar app color="surface" flat density="comfortable" class="app-header">
    <router-link to="/" class="d-flex align-center text-decoration-none">
      <v-img
        src="@/assets/logo.png"
        max-height="40"
        max-width="40"
        contain
        class="ml-4 mr-2 app-logo"
        alt="App Logo"
      ></v-img>
      <div class="app-title">
        <span class="font-weight-bold text-h6 text-primary">美味秘籍</span>
      </div>
    </router-link>

    <v-spacer></v-spacer>

    <!-- Use icon buttons directly on larger screens now -->
    <v-btn icon to="/random" class="header-button d-none d-sm-flex">
      <v-icon>mdi-dice-5-outline</v-icon>
    </v-btn>
    <v-btn icon @click="showMenuDialog = true" class="header-button d-none d-sm-flex">
      <v-badge
        :content="todayMenu.count"
        :model-value="todayMenu.count > 0"
        color="error"
        floating
        dot
      >
        <v-icon>mdi-silverware-fork-knife</v-icon>
      </v-badge>
    </v-btn>

    <!-- Buttons for smaller screens -->
    <v-btn icon to="/random" class="d-sm-none mx-1">
      <v-icon>mdi-dice-5-outline</v-icon>
    </v-btn>
    <v-btn icon @click="showMenuDialog = true" class="d-sm-none mx-1">
      <v-badge
        :content="todayMenu.count"
        :model-value="todayMenu.count > 0"
        color="error"
        floating
        dot
      >
        <v-icon>mdi-silverware-fork-knife</v-icon>
      </v-badge>
    </v-btn>

    <v-menu offset-y>
      <template v-slot:activator="{ props }">
        <v-btn text v-bind="props" class="user-menu-button ml-2 mr-2">
          <v-avatar color="primary" size="32" class="mr-2">
            <span class="white--text text-caption">用户</span>
          </v-avatar>
          <span class="d-none d-md-inline">用户名</span> 
          <v-icon right class="d-none d-md-inline ml-1">mdi-chevron-down</v-icon>
        </v-btn>
      </template>
      <v-list density="compact" nav>
        <v-list-item link @click="() => {}">
          <template v-slot:prepend>
            <v-icon>mdi-account-circle-outline</v-icon>
          </template>
          <v-list-item-title>个人中心</v-list-item-title>
        </v-list-item>
        <v-list-item link @click="() => {}">
          <template v-slot:prepend>
            <v-icon>mdi-cog-outline</v-icon>
          </template>
          <v-list-item-title>设置</v-list-item-title>
        </v-list-item>
        <v-divider class="my-1"></v-divider>
        <v-list-item link @click="() => {}">
          <template v-slot:prepend>
            <v-icon color="error">mdi-logout</v-icon>
          </template>
          <v-list-item-title class="text-error">退出登录</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>

    <!-- Today's Menu Dialog -->
    <TodayMenuDialog
      v-model="showMenuDialog"
      :items="todayMenu.allItems"
      @remove="handleRemoveRecipe"
      @clear-all="handleClearAll"
      @clear-checked="handleClearChecked"
    />
  </v-app-bar>
</template>

<script setup>
import { ref } from 'vue';
import { useTodayMenuStore } from '@/stores/todayMenu';
import TodayMenuDialog from '@/components/TodayMenuDialog.vue';

const todayMenu = useTodayMenuStore();
const showMenuDialog = ref(false);

// Methods for TodayMenuDialog
const handleRemoveRecipe = (recipeId) => {
  todayMenu.removeRecipe(recipeId);
};

const handleClearAll = () => {
  todayMenu.clearAll();
};

const handleClearChecked = () => {
  todayMenu.clearChecked();
};
</script>

<style scoped>
@import '@/assets/components/app-header.css';
</style>
