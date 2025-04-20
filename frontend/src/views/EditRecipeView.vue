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
              <!-- Update Status Indicators -->
              <v-overlay :model-value="isUpdating" class="align-center justify-center">
                <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
              </v-overlay>
              <v-snackbar v-model="showUpdateError" color="error" timeout="5000">
                {{ updateErrorMsg }}
                <template v-slot:actions>
                  <v-btn color="white" variant="text" @click="showUpdateError = false">
                    关闭
                  </v-btn>
                </template>
              </v-snackbar>
            </div>
          </v-fade-transition>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { ref, onMounted, computed } from 'vue'; // Import computed
import { useRoute, useRouter } from 'vue-router';
import RecipeForm from '@/components/RecipeForm.vue';
import { getRecipeById, updateRecipe, uploadRecipeImage } from '@/services/api'; // Import uploadRecipeImage

export default {
  name: 'EditRecipeView',
  components: {
    RecipeForm,
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const recipeData = ref(null);
    const loading = ref(true); // Start loading initially
    const error = ref(null);
    const isUpdating = ref(false); // State for update operation
    const showUpdateError = ref(false);
    const updateErrorMsg = ref('');

    // Get recipe ID from route params safely
    const recipeId = computed(() => route.params.id);

    const fetchRecipeData = async () => {
      loading.value = true;
      error.value = null; // Reset error before fetching
      if (!recipeId.value) {
          error.value = new Error("未在路由参数中找到菜谱ID。");
          loading.value = false;
          return;
      }
      try {
        const response = await getRecipeById(recipeId.value);
        // Ensure response.data exists and is an object
        if (response && typeof response.data === 'object' && response.data !== null) {
           recipeData.value = response.data;
        } else {
           // Handle cases where data might be missing or in unexpected format
           throw new Error("从API接收到的菜谱数据格式无效。");
        }
      } catch (err) {
        console.error("获取待编辑菜谱数据失败:", err);
        error.value = err; // Set error state to display message
      } finally {
        loading.value = false;
      }
    };

    const handleUpdateRecipe = async ({ recipeData: updatedData, imageFile }) => {
      if (!recipeId.value) {
        updateErrorMsg.value = "无法更新：缺少菜谱ID。";
        showUpdateError.value = true;
        return;
      }

      isUpdating.value = true;
      showUpdateError.value = false;
      updateErrorMsg.value = '';


      try {
        // Step 1: Update recipe text data
        // Pass only the updatedData part to updateRecipe
        await updateRecipe(recipeId.value, updatedData); 
        // updateSuccess = true; // Removed assignment to unused variable

        // Step 2: If an image file was provided, upload it
        if (imageFile) {
          try {
            await uploadRecipeImage(recipeId.value, imageFile);
            // Image uploaded successfully
          } catch (uploadError) {
            console.error('图片上传失败:', uploadError);
            // Even if image upload fails, the text data was updated.
            // Show a specific error message but still navigate.
            updateErrorMsg.value = `菜谱信息已更新，但图片上传失败: ${uploadError.message || '未知错误'}`;
            showUpdateError.value = true;
            // Do not throw here, allow navigation
          }
        }

        // Step 3: Navigate only if the text update was successful
        router.push({ name: 'recipe-detail', params: { id: recipeId.value } });

      } catch (mainUpdateError) {
        console.error("更新菜谱失败:", mainUpdateError);
        updateErrorMsg.value = `更新失败: ${mainUpdateError.message || '请稍后重试'}`;
        showUpdateError.value = true;
      } finally {
        isUpdating.value = false;
      }
    };

    const goBack = () => {
      // Navigate back to the recipe detail page if possible, otherwise home
      if (recipeId.value) {
        router.push({ name: 'recipe-detail', params: { id: recipeId.value } });
      } else {
        router.push({ name: 'home' }); // Fallback to home
      }
    };

    // Fetch data when the component mounts
    onMounted(() => {
      fetchRecipeData();
    });

    return {
      recipeData,
      loading,
      error,
      isUpdating, // Expose update loading state
      showUpdateError, // Expose error snackbar state
      updateErrorMsg, // Expose error message
      handleUpdateRecipe,
      goBack,
    };
  },
};
</script>

<style scoped>
@import '@/assets/views/edit-recipe-view.css';
</style>
