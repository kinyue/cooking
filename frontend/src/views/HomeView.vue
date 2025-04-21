<template>
  <v-container fluid class="pa-5">


    <v-row class="mt-4"> <!-- Added margin-top to compensate for removed header row -->
      <v-col v-for="recipe in recipes" :key="recipe.id" cols="12" sm="6" md="4" lg="3">
        <RecipeCard :recipe="recipe" @recipeDeleted="handleRecipeDeleted" v-model:snackbar="snackbar" />
      </v-col>

      <v-col v-if="loading" cols="12" class="text-center">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
        <p class="mt-2">加载中...</p>
      </v-col>

      <v-col v-if="error" cols="12">
        <v-alert type="error" variant="tonal">
          加载菜谱失败：{{ error.message || '请稍后再试' }}
        </v-alert>
      </v-col>

      <v-col v-if="!loading && !error && recipes.length === 0" cols="12" class="text-center text-grey">
        <p>暂无推荐菜谱。</p>
      </v-col>
    </v-row>

    <!-- Pagination Controls -->
    <v-row v-if="!loading && !error && totalPages > 1" justify="center" class="pagination-row">
      <v-col cols="auto">
        <v-pagination v-model="currentPage" :length="totalPages" :total-visible="$vuetify.display.mdAndUp ? 7 : 3"
          density="comfortable" rounded="circle" active-color="primary" size="large"
          class="custom-pagination"></v-pagination>
      </v-col>
    </v-row>
  </v-container>

  <!-- Global Snackbar -->
  <v-snackbar v-model="snackbar.show" :color="snackbar.color" :timeout="3000" location="top" elevation="4" rounded="lg"
    transition="slide-y-transition">
    <template v-slot:default>
      <div class="d-flex align-center">
        <v-icon :icon="snackbar.color === 'success' ? 'mdi-check-circle' : 'mdi-alert-circle'" start
          class="mr-2"></v-icon>
        <div>
          <div class="text-subtitle-2 font-weight-medium">
            {{ snackbar.color === 'success' ? '操作成功' : '操作失败' }}
          </div>
          <div class="text-body-2">{{ snackbar.text }}</div>
        </div>
      </div>
    </template>
  </v-snackbar>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'; // Import useRouter
import { ref, onMounted, watch } from 'vue'; // Import watch
import RecipeCard from '@/components/RecipeCard.vue';
import api from '@/services/api';

// --- State ---
const route = useRoute(); // Re-add route instance
const router = useRouter(); 
const snackbar = ref({
  show: false,
  text: '',
  color: 'success'
});
const recipes = ref([]);
const loading = ref(false);
const error = ref(null);

// --- Pagination State ---
const itemsPerPage = 8; // Items per page
const currentPage = ref(1);
const totalPages = ref(1);

// --- Methods ---
const fetchRecipes = async (page = 1) => {
  loading.value = true;
  error.value = null;
  try {
    // 构建筛选参数
    const params = {
      page,
      limit: itemsPerPage,
      ...route.query.search && { search: route.query.search },
      ...route.query.ingredients && { ingredients: route.query.ingredients }, // Add ingredients param
      ...route.query.tags && { tags: route.query.tags }, // Pass the array directly if it exists
      ...route.query.difficulty && { difficulty: route.query.difficulty },
      ...route.query.cuisine && { cuisine: route.query.cuisine },
      ...route.query.prepTimeMin && { prepTimeMin: Number(route.query.prepTimeMin) },
      ...route.query.prepTimeMax && { prepTimeMax: Number(route.query.prepTimeMax) },
      ...route.query.cookTimeMin && { cookTimeMin: Number(route.query.cookTimeMin) },
      ...route.query.cookTimeMax && { cookTimeMax: Number(route.query.cookTimeMax) },
      ...route.query.servingsMin && { servingsMin: Number(route.query.servingsMin) },
      ...route.query.servingsMax && { servingsMax: Number(route.query.servingsMax) }
    };

    // 调用API获取筛选后的数据
    const response = await api.getRecipes(params);
    recipes.value = response.data; // The list of recipes for the current page
    // Update pagination state from the response
    if (response.pagination) {
      currentPage.value = response.pagination.current_page;
      totalPages.value = response.pagination.total_pages;
    } else {
      // Handle case where pagination info might be missing (e.g., error or older API version)
      totalPages.value = 1; // Default to 1 page if pagination info is absent
    }
  } catch (err) {
    console.error("Failed to fetch recipes:", err);
    error.value = err;
    recipes.value = [];
    totalPages.value = 1; // Reset pages on error
  } finally {
    loading.value = false;
  }
};



// Handler for recipe deletion from RecipeCard
const handleRecipeDeleted = async (recipeId) => {
  // After deletion, refetch the current page to reflect changes
  // This handles cases where deleting the last item on a page should potentially move to the previous page,
  // or just refresh the current view. Fetching the current page number is simplest.
  // We might need the name for the snackbar *before* refetching.
  const deletedRecipe = recipes.value.find(r => r.id === recipeId);
  const deletedRecipeName = deletedRecipe ? deletedRecipe.name : '该菜谱';

  await fetchRecipes(currentPage.value);

  // Show snackbar confirmation (assuming the child component doesn't already do this via v-model)
  // If the child component handles the snackbar via v-model:snackbar, this might be redundant.
  // Let's keep it for now, assuming HomeView manages its own snackbar state upon deletion confirmation.
  snackbar.value = {
    show: true,
    text: `菜谱 "${deletedRecipeName}" 已删除`,
    color: 'success'
  };
};


// --- Watchers ---
// Watch for changes in the current page and fetch new data
watch(currentPage, (newPage, oldPage) => {
  // Avoid fetching again if the page number hasn't actually changed
  if (newPage !== oldPage) {
    fetchRecipes(newPage);
  }
});
 
// Watch for the 'added' query parameter to refresh the list
watch(() => route.query.added, (newVal) => {
  if (newVal) {
    fetchRecipes(1); // Refresh the first page
    // Create a copy of the current query, remove 'added', then replace
    const query = { ...route.query };
    delete query.added;
    router.replace({ query });
  }
}, { immediate: false }); // Don't run immediately on mount

// Watch for filter changes in route query
watch(() => route.query, (newQuery) => {
  // 忽略仅包含 _t 参数的变化（这是为了确保路由更新而添加的时间戳）
  const hasOnlyTimestamp = Object.keys(newQuery).length === 1 && newQuery._t;
  if (!hasOnlyTimestamp) {
    currentPage.value = 1; // 重置页码
    fetchRecipes(1);
  }
}, { deep: true });
 
 // --- Lifecycle Hooks ---
 onMounted(() => {
   // Fetch the first page on component mount
   fetchRecipes(1);
 
   const deletedRecipe = route.query.deletedRecipe;
  if (deletedRecipe) {
    snackbar.value = {
      show: true,
      text: `菜谱 "${deletedRecipe}" 已删除`,
      color: 'success'
    };
  }
});
</script>

<style scoped>
@import '@/assets/views/home-view.css';

.pagination-row {
  margin-top: 32px;
  margin-bottom: 16px;
}

/* Custom styles for pagination buttons */
:deep(.custom-pagination) {
  .v-pagination__item {
    font-weight: 500;
    min-width: 40px;
    height: 40px;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;

    &::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: currentColor;
      opacity: 0;
      transition: opacity 0.25s ease;
    }

    &--active {
      font-weight: 600;
      transform: scale(1.1);
      box-shadow: 0 2px 8px rgba(var(--v-theme-primary), 0.25);
    }

    &:not(.v-pagination__item--active):hover {
      background: rgba(var(--v-theme-primary), 0.05);
      transform: translateY(-1px);
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
  }

  /* Responsive adjustments */
  @media (max-width: 600px) {
    .v-pagination__item {
      min-width: 36px;
      height: 36px;
      margin: 0 2px;
    }
  }

  /* Navigation arrows */
  .v-pagination__prev,
  .v-pagination__next {
    transition: transform 0.2s ease;

    &:hover {
      transform: scale(1.1);
    }
  }
}
</style>
