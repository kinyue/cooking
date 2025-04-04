<template>
  <v-container fluid class="pa-5">
    <v-row justify="center">
      <v-col cols="12" md="8" lg="7">
        <div class="edit-recipe-container">
          <div class="edit-recipe-header">
            <h2 class="edit-recipe-title font-weight-medium">
              <v-icon icon="mdi-pencil" class="mr-2"></v-icon>
              编辑菜谱
            </h2>
          </div>

          <!-- Loading Indicator -->
          <v-fade-transition>
            <div v-if="loading" class="loading-container">
              <v-progress-circular
                size="42"
                width="4"
                indeterminate
                color="primary"
              ></v-progress-circular>
              <span class="loading-text">加载菜谱数据...</span>
            </div>
          </v-fade-transition>

          <!-- Error Message -->
          <v-fade-transition>
            <div v-if="error">
              <v-alert
                type="error"
                variant="tonal"
                title="加载失败"
                :text="`加载菜谱数据失败: ${error.message || '请稍后重试。'}`"
                class="mb-4"
                border="start"
                density="comfortable"
              ></v-alert>
            </div>
          </v-fade-transition>

          <!-- Recipe Form - Render only when data is loaded -->
          <v-fade-transition>
            <div v-if="recipeData && !loading">
              <RecipeForm
                formType="edit"
                :initialData="recipeData"
                @submit="handleUpdateRecipe"
                @cancel="goBack"
              />
            </div>
          </v-fade-transition>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import RecipeForm from '@/components/RecipeForm.vue';
import { getRecipeById } from '@/services/api';
import { updateRecipe } from '@/services/api'; 
// TODO: Import updateRecipe from api service when implemented

export default {
  name: 'EditRecipeView',
  components: {
    RecipeForm,
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const recipeData = ref(null);
    const loading = ref(false);
    const error = ref(null);

    const fetchRecipeData = async () => {
      loading.value = true;
      error.value = null;
      try {
        const recipeId = route.params.id;
        if (!recipeId) {
          throw new Error("Recipe ID not found in route parameters.");
        }
        const response = await getRecipeById(recipeId);
        recipeData.value = response.data; 
      } catch (err) {
        console.error("Failed to fetch recipe data for editing:", err);
        error.value = err;
      } finally {
        loading.value = false;
      }
    };

    const handleUpdateRecipe = async (updatedRecipeData) => {

      if (!recipeData.value?.id) {
         console.error("Cannot update recipe: ID is missing.");
         alert("无法更新菜谱：缺少菜谱ID。");
         return;
      }

      try {
        await updateRecipe(recipeData.value.id, updatedRecipeData);
        // Navigate on success
        router.push({ name: 'recipe-detail', params: { id: recipeData.value.id } });
      } catch (updateError) {
        console.error("Failed to update recipe:", updateError);
        // Handle update error (e.g., show a snackbar or alert)
        alert(`更新失败: ${updateError.message || '请稍后重试'}`); 
      }
    };

    const goBack = () => {
      // Check if the previous page was a recipe detail page
      const previousPath = window.history.state?.back;
      const recipeId = route.params.id; // Get current recipe ID for comparison
      
      // Check if previousPath exists, includes '/recipes/', and is not the base '/recipes/' path
      // Also ensure the previous path ID matches the current recipe ID to confirm it's the detail page for *this* recipe
      if (previousPath && previousPath.includes(`/recipes/${recipeId}`)) {
         router.back(); // Go back to the recipe detail page
      } else {
         router.push('/'); // Go back to the home page
      }
    };

    onMounted(() => {
      fetchRecipeData();
    });

    return {
      recipeData,
      loading,
      error,
      handleUpdateRecipe,
      goBack,
    };
  },
};
</script>

<style scoped>
@import '@/assets/views/edit-recipe-view.css';
</style>
