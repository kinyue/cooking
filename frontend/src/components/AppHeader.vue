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

    <!-- Filter button for larger screens -->
    <v-btn icon @click="showFilterDrawer = true" class="header-button d-none d-sm-flex">
      <v-icon>mdi-filter-variant</v-icon>
    </v-btn>

    <!-- Use icon buttons directly on larger screens now -->
    <v-btn icon @click="isRandomRecipeDialogOpen = true" class="header-button d-none d-sm-flex">
      <v-icon>mdi-dice-5-outline</v-icon>
    </v-btn>
    <!-- Bind click event to open the add dialog -->
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
    <!-- Calendar Button for larger screens -->
    <v-btn icon @click="openCalendar" class="header-button d-none d-sm-flex">
      <v-icon>mdi-calendar-month-outline</v-icon>
    </v-btn>

    <!-- Buttons for smaller screens -->
    <!-- Filter button for smaller screens -->
    <v-btn icon @click="showFilterDrawer = true" class="d-sm-none mx-1">
      <v-icon>mdi-filter-variant</v-icon>
    </v-btn>
    <v-btn icon @click="isRandomRecipeDialogOpen = true" class="d-sm-none mx-1">
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
    <!-- Calendar Button for smaller screens -->
    <v-btn icon @click="openCalendar" class="d-sm-none mx-1">
      <v-icon>mdi-calendar-month-outline</v-icon>
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

    <!-- Today's Menu Dialog - No longer needs items prop or old event listeners -->
    <TodayMenuDialog
      v-model="showMenuDialog"
      @update:snackbar="snackbar = $event" 
    />
    <!-- Note: Pass snackbar updates if TodayMenuDialog emits them -->
    <!-- If TodayMenuDialog handles its own snackbar, remove @update:snackbar -->

    <!-- Random Recipe Dialog -->
    <RandomRecipeDialog v-model="isRandomRecipeDialogOpen" />

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

    <!-- Filter Drawer -->
    <FilterDrawer 
      v-model="showFilterDrawer"
      @apply="handleFilterApply"
    />

    <!-- Snackbar for feedback -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="snackbar.timeout"
      location="top"
      elevation="4"
      rounded="lg"
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

    <!-- Calendar Dialog -->
    <v-dialog v-model="showCalendarDialog" width="auto">
      <v-card>
        <v-card-title>选择日期查看菜单</v-card-title>
        <v-date-picker
          v-model="selectedDate"
          @update:modelValue="handleDateSelect"
          :events="datesWithMenus"
          event-color="primary"
          color="primary"
          show-adjacent-months
          hide-header
          class="ma-2"
        ></v-date-picker>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="showCalendarDialog = false">关闭</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-app-bar>
</template>

<script setup>
import { ref, computed } from 'vue'; // Import computed
import { useTodayMenuStore } from '@/stores/todayMenu';
import TodayMenuDialog from '@/components/TodayMenuDialog.vue';
import RandomRecipeDialog from '@/components/RandomRecipeDialog.vue';
import RecipeForm from '@/components/RecipeForm.vue';
import FilterDrawer from '@/components/FilterDrawer.vue';
// Remove direct api import for create/upload, use composable instead
// import api from '@/services/api';
import { useRouter } from 'vue-router';
import { useRecipeSubmit } from '@/composables/useRecipeSubmit'; // Import the composable

const todayMenu = useTodayMenuStore();
const showMenuDialog = ref(false);
const showAddDialog = ref(false);
const isRandomRecipeDialogOpen = ref(false);
const showFilterDrawer = ref(false);
const router = useRouter();

// --- Calendar Dialog State & Logic ---
const showCalendarDialog = ref(false);
const selectedDate = ref(new Date()); // Initialize with today or null
const datesWithMenus = computed(() => todayMenu.daysWithSavedMenu); // Get dates from store

// Snackbar state
const snackbar = ref({
  show: false,
  text: '',
  color: 'success',
  timeout: 3000
});

// Remove unused methods related to old TodayMenuDialog events
// const handleRemoveRecipe = (recipeId) => { ... };
// const handleClearAll = () => { ... };
// const handleClearChecked = () => { ... };

// --- Calendar Dialog Methods ---
const openCalendar = async () => {
  // Load dates with menus when opening the calendar
  await todayMenu.loadDatesWithMenus();
  // Ensure selectedDate is initialized (e.g., to today or store's current date)
  selectedDate.value = new Date(todayMenu.currentDate); // Sync with store's current date
  showCalendarDialog.value = true;
};

const handleDateSelect = async (date) => {
  if (!date) return;
  // Format the selected date (assuming 'date' is a Date object from v-date-picker)
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const dateString = `${year}-${month}-${day}`;

  // Update store's state for the viewed historical date
  // NOTE: We are NOT loading the data here, the target view/dialog will do that.
  // We just set the date context in the store if needed, or pass it via route param.
  // Let's assume the target view will use the route param.

  // Close calendar and navigate to the historical menu view
  showCalendarDialog.value = false;
  router.push({ name: 'historical-menu', params: { date: dateString } });
};

// --- Use the composable for submission logic ---
// Only destructure what's needed: submitError and submitRecipe
const { error: submitError, submitRecipe } = useRecipeSubmit();

// --- Methods for Add Recipe Dialog ---
const handleAddRecipeSubmit = async (payload) => {
  // Call the composable's submit function
  const newRecipeId = await submitRecipe(payload);

  if (newRecipeId) {
    // Success
    showAddDialog.value = false;
    snackbar.value = {
      show: true,
      // We don't have the recipe name directly here anymore, use generic message
      text: `新菜谱添加成功！ (ID: ${newRecipeId})`,
      color: 'success',
      timeout: 3000,
    };
    // Navigate to home page to trigger refresh
    router.push({ path: '/', query: { added: Date.now() } });
    // Or navigate to detail page:
    // router.push({ name: 'recipe-detail', params: { id: newRecipeId } });
  } else {
    // Failure - error message is in submitError.value from the composable
    snackbar.value = {
      show: true,
      text: `添加菜谱失败: ${submitError.value || '请稍后再试'}`,
      color: 'error',
      timeout: 5000,
    };
    // Keep the dialog open on error
  }
};

const handleCancelAdd = () => {
  showAddDialog.value = false;
};

// --- Methods for Filter Drawer ---
const handleFilterApply = (filters) => {
  // 将筛选条件转换为URL查询参数
  const query = {
    ...(filters.search && { search: filters.search }),
    ...(filters.ingredientSearch && { ingredients: filters.ingredientSearch }), // Add ingredient search query param
    ...(filters.tags?.length > 0 && { tags: filters.tags }), // Pass the array directly
    ...(filters.difficulty && { difficulty: filters.difficulty }),
    ...(filters.cuisine && { cuisine: filters.cuisine }),
    ...(filters.prepTimeRange && { 
      prepTimeMin: filters.prepTimeRange[0],
      prepTimeMax: filters.prepTimeRange[1]
    }),
    ...(filters.cookTimeRange && {
      cookTimeMin: filters.cookTimeRange[0],
      cookTimeMax: filters.cookTimeRange[1]
    }),
    ...(filters.servings && {
      servingsMin: filters.servings[0],
      servingsMax: filters.servings[1]
    }),
    // 添加时间戳以确保路由更新
    _t: Date.now()
  };

  // 更新路由以触发HomeView组件的数据刷新
  router.push({ 
    path: '/',
    query
  });

  // 显示成功提示
  snackbar.value = {
    show: true,
    text: '筛选条件已应用',
    color: 'success',
    timeout: 2000
  };
};

</script>

<style scoped>
@import '@/assets/components/app-header.css';
</style>
