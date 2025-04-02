<template>
  <v-container fluid class="pa-5">
    <v-row justify="center">
      <v-col cols="12" md="8">
        <h2 class="text-h5 font-weight-medium mb-4">编辑菜谱</h2>

        <!-- Loading Indicator -->
        <v-row v-if="loading" justify="center" align="center" style="min-height: 200px;">
          <v-col cols="12" class="text-center">
            <v-progress-circular indeterminate color="primary"></v-progress-circular>
            <p class="mt-2 text-medium-emphasis">加载菜谱数据...</p>
          </v-col>
        </v-row>

        <!-- Error Message -->
        <v-row v-else-if="error" justify="center">
          <v-col cols="12">
            <v-alert
              type="error"
              variant="tonal"
              title="加载失败"
              :text="`加载菜谱数据失败: ${error.message || '请稍后重试。'}`"
              class="mb-4"
            ></v-alert>
          </v-col>
        </v-row>

        <!-- Recipe Form - Render only when data is loaded -->
        <RecipeForm
          v-if="recipeData && !loading"
          formType="edit"
          :initialData="recipeData"
          @submit="handleUpdateRecipe"
          @cancel="goBack"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import RecipeForm from '@/components/RecipeForm.vue';
import { getRecipeById } from '@/services/api'; // Assuming updateRecipe exists
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
        recipeData.value = response.data; // Assuming API returns { data: recipeObject }
      } catch (err) {
        console.error("Failed to fetch recipe data for editing:", err);
        error.value = err;
      } finally {
        loading.value = false;
      }
    };

    const handleUpdateRecipe = async (updatedRecipeData) => {
      console.log('Submitting updated recipe:', updatedRecipeData);
      // TODO: Implement API call to update the recipe
      // try {
      //   const response = await updateRecipe(recipeData.value.id, updatedRecipeData);
      //   // Navigate on success
      //   router.push({ name: 'recipe-detail', params: { id: recipeData.value.id } });
      // } catch (updateError) {
      //   console.error("Failed to update recipe:", updateError);
      //   // Handle update error (e.g., show a snackbar)
      // }
       alert('更新功能尚未实现！'); // Placeholder
       router.push({ name: 'recipe-detail', params: { id: recipeData.value.id } }); // Navigate back for now
    };

    const goBack = () => {
      router.back();
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
