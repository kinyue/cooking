<template>
  <v-container fluid class="pa-5">
    <v-row align="center" class="mb-4">
      <v-col cols="12" sm="auto">
        <h1 class="text-h5 font-weight-medium">推荐菜谱</h1>
      </v-col>
      <v-spacer></v-spacer>
      <!-- <v-col cols="6" sm="3" md="2">
        <v-select
          v-model="recommendCount"
          :items="countOptions"
          label="推荐数量"
          density="compact"
          variant="outlined"
          hide-details
        ></v-select>
      </v-col> -->
      <!-- <v-col cols="6" sm="auto">
        <v-btn color="primary" @click="startRecommendation" size="large">
          <v-icon left icon="mdi-play-circle-outline" class="mr-1"></v-icon>
          开始推荐
        </v-btn>
      </v-col> -->
      <v-col cols="6" sm="auto">
        <v-btn color="primary" @click="showAddDialog = true" size="large">
          <v-icon left icon="mdi-plus-circle-outline" class="mr-1"></v-icon>
          添加菜谱
        </v-btn>
      </v-col>
    </v-row>

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

    <v-row>
      <v-col
        v-for="recipe in recipes"
        :key="recipe.id"
        cols="12"
        sm="6"
        md="4"
        lg="3"
      >
        <RecipeCard
          :recipe="recipe"
          @recipeDeleted="handleRecipeDeleted"
          v-model:snackbar="snackbar"
        />
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
        <v-pagination
          v-model="currentPage"
          :length="totalPages"
          :total-visible="$vuetify.display.mdAndUp ? 7 : 3"
          density="comfortable"
          rounded="circle"
          active-color="primary"
          size="large"
          class="custom-pagination"
        ></v-pagination>
      </v-col>
    </v-row>
  </v-container>

  <!-- Global Snackbar -->
  <v-snackbar
    v-model="snackbar.show"
    :color="snackbar.color"
    :timeout="3000"
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
</template>

<script setup>
import { useRoute } from 'vue-router';
import { ref, onMounted, watch } from 'vue'; // Import watch
import RecipeCard from '@/components/RecipeCard.vue';
import RecipeForm from '@/components/RecipeForm.vue';
import api from '@/services/api';

// --- State ---
const route = useRoute();
const showAddDialog = ref(false);
const snackbar = ref({
  show: false,
  text: '',
  color: 'success'
});
// const recommendCount = ref(12);
// const countOptions = ref([4, 8, 12, 16, 20, 24]);
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
    // Pass page and limit to the API call
    const response = await api.getRecipes({ page: page, limit: itemsPerPage });
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


// const startRecommendation = () => {
  // console.log(`Starting recommendation with count: ${recommendCount.value}`);
  // fetchRecipes(recommendCount.value);
// };


// Handler for RecipeForm submission (Add mode)
const handleAddRecipeSubmit = async (formData) => {
  try {
    const result = await api.createRecipe(formData);
    showAddDialog.value = false;
    // Fetch the first page after adding a new recipe
    await fetchRecipes(1);
    snackbar.value = {
      show: true,
      text: `菜谱 "${result.data.name}" 添加成功！`,
      color: 'success'
    };
  } catch (err) {
    console.error("Failed to add recipe:", err);
    snackbar.value = {
      show: true,
      text: `添加菜谱失败: ${err.response?.data?.description || err.message || '请稍后再试'}`,
      color: 'error'
    };
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

// Handler for canceling the add recipe dialog
const handleCancelAdd = () => {
  showAddDialog.value = false;
};

// --- Watchers ---
// Watch for changes in the current page and fetch new data
watch(currentPage, (newPage, oldPage) => {
  // Avoid fetching again if the page number hasn't actually changed
  // This can happen during initial setup or if the value is programmatically set without a real change
  if (newPage !== oldPage) {
     fetchRecipes(newPage);
  }
});

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
