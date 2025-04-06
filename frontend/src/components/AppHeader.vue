<template>
  <v-app-bar app color="surface" flat class="app-header">
    <router-link to="/" class="d-flex align-center text-decoration-none">
      <v-img
        src="@/assets/logo.png"
        max-height="48"
        max-width="48"
        contain
        class="ml-4 mr-3 app-logo"
        alt="App Logo"
      ></v-img>
      <div class="app-title">
        <span class="font-weight-bold text-h5 text-primary">美味秘籍</span>
      </div>
    </router-link>

    <v-spacer></v-spacer>

    <!-- Use icon buttons directly on larger screens now -->
    <v-btn icon to="/random" class="header-button d-none d-sm-flex">
      <v-icon>mdi-dice-5-outline</v-icon>
    </v-btn>
    <!-- Bind click event to open the dialog -->
    <v-btn icon @click="showAddDialog = true" class="header-button d-none d-sm-flex">
      <v-icon>mdi-hamburger-plus</v-icon>
    </v-btn>
    <v-btn icon @click="showMenuDialog = true" class="header-button d-none d-sm-flex">
      <v-badge
        :content="todayMenu.count" 
        :model-value="todayMenu.count > 0"
        color="error"
        floating
        overlap 
      >
        <v-icon>mdi-silverware-fork-knife</v-icon>
      </v-badge>
    </v-btn>

    <!-- Buttons for smaller screens -->
    <v-btn icon to="/random" class="d-sm-none mx-1">
      <v-icon>mdi-dice-5-outline</v-icon>
    </v-btn>
    <!-- Add Recipe Button for smaller screens -->
    <v-btn icon @click="showAddDialog = true" class="d-sm-none mx-1">
      <v-icon>mdi-hamburger-plus</v-icon>
    </v-btn>
    <v-btn icon @click="showMenuDialog = true" class="d-sm-none mx-1">
      <v-badge
        :content="todayMenu.count" 
        :model-value="todayMenu.count > 0"
        color="error"
        floating
        overlap 
      >
        <v-icon>mdi-silverware-fork-knife</v-icon>
      </v-badge>
    </v-btn>

    <!-- <v-menu offset-y>
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
    </v-menu> -->

    <!-- Today's Menu Dialog -->
    <TodayMenuDialog
      v-model="showMenuDialog"
      :items="todayMenu.allItems"
      @remove="handleRemoveRecipe"
      @clear-all="handleClearAll"
      @clear-checked="handleClearChecked"
    />

    <!-- Add Recipe Dialog -->
    <v-dialog v-model="showAddDialog" persistent max-width="800px">
      <v-card>
        <v-card-title>
          <span class="text-h5">添加新菜谱</span>
        </v-card-title>
        <v-card-text>
          <RecipeForm @submit="handleAddRecipeSubmit" @cancel="handleCancelAdd" />
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- Snackbar for feedback -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="snackbar.timeout"
      location="top"
      elevation="4"
      rounded="lg"
      variant="tonal"
      transition="slide-y-transition"
    >
      <template v-slot:default>
        <div class="d-flex align-center">
          <v-icon
            :icon="snackbar.color === 'success' ? 'mdi-check-circle' : 'mdi-alert-circle'"
            start
            class="mr-2"
          ></v-icon>
          <div>
            <div class="text-subtitle-2 font-weight-medium">
              {{ snackbar.color === 'success' ? '操作成功' : '操作失败' }}
            </div>
            <div class="text-body-2">{{ snackbar.text }}</div>
          </div>
        </div>
      </template>
    </v-snackbar>

  </v-app-bar>
</template>

<script setup>
import { ref } from 'vue';
import { useTodayMenuStore } from '@/stores/todayMenu';
import TodayMenuDialog from '@/components/TodayMenuDialog.vue';
import RecipeForm from '@/components/RecipeForm.vue'; // Import RecipeForm
import api from '@/services/api'; // Import api service
import { useRouter } from 'vue-router'; // Import useRouter

const todayMenu = useTodayMenuStore();
const showMenuDialog = ref(false);
const showAddDialog = ref(false); // State for Add Recipe Dialog
const router = useRouter(); // Get router instance

// Snackbar state
const snackbar = ref({
  show: false,
  text: '',
  color: 'success',
  timeout: 3000
});

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

// --- Methods for Add Recipe Dialog ---
const handleAddRecipeSubmit = async (formData) => {
  try {
    const result = await api.createRecipe(formData);
    showAddDialog.value = false;
    // Show success snackbar
    snackbar.value = {
      show: true,
      text: `菜谱 "${result.data.name}" 添加成功！`,
      color: 'success',
      timeout: 3000
    };
    // Navigate back to the home page with a query param to trigger refresh
    // Using Date.now() ensures the query value changes each time, reliably triggering watchers
    router.push({ path: '/', query: { added: Date.now() } }); 
  } catch (err) {
    console.error("Failed to add recipe:", err);
    // Show error snackbar
    snackbar.value = {
      show: true,
      text: `添加菜谱失败: ${err.response?.data?.description || err.message || '请稍后再试'}`,
      color: 'error',
      timeout: 3000
    };
  }
};

const handleCancelAdd = () => {
  showAddDialog.value = false;
};

</script>

<style scoped>
@import '@/assets/components/app-header.css';
</style>
