<template>
  <v-container class="add-recipe-view">
    <v-row justify="center">
      <v-col cols="12" md="8" lg="6">
        <h1 class="view-title">创建新菜谱</h1>
        <v-card class="pa-4 pa-md-6" elevation="2">
          <RecipeForm @submit="handleSubmit" @cancel="handleCancel" />
          <!-- Use isSubmitting from composable for overlay -->
          <v-overlay :model-value="isSubmitting" class="align-center justify-center">
            <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
          </v-overlay>
          <!-- Use local state for snackbar -->
          <v-snackbar v-model="showErrorSnackbar" color="error" timeout="5000">
            {{ snackbarMessage }}
            <template v-slot:actions>
              <v-btn color="white" variant="text" @click="showErrorSnackbar = false">
                关闭
              </v-btn>
            </template>
          </v-snackbar>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, watch } from 'vue'; // Import watch
import { useRouter } from 'vue-router';
import RecipeForm from '@/components/RecipeForm.vue';
// Remove direct api imports, use composable instead
// import { createRecipe, uploadRecipeImage } from '@/services/api';
import { useRecipeSubmit } from '@/composables/useRecipeSubmit'; // Import the composable

const router = useRouter();
// Use state from the composable
const { isSubmitting, error: submitError, submitRecipe } = useRecipeSubmit();

// Local state for error display in this view
const showErrorSnackbar = ref(false);
const snackbarMessage = ref('');

// Watch for errors from the composable to show the snackbar
watch(submitError, (newError) => {
  if (newError) {
    snackbarMessage.value = `创建失败: ${newError}`;
    showErrorSnackbar.value = true;
  } else {
    showErrorSnackbar.value = false; // Hide snackbar if error is cleared
  }
});

// Handle the submit event from RecipeForm
const handleSubmit = async (payload) => {
  // Call the composable's submit function
  const newRecipeId = await submitRecipe(payload);

  if (newRecipeId) {
    // Success: Navigate to the detail page
    router.push({ name: 'recipe-detail', params: { id: newRecipeId } });
  }
  // Failure: Error handling is done via the watch on submitError
};

const handleCancel = () => {
  // Navigate back or to home page
  router.back() || router.push({ name: 'home' });
};
</script>

<style scoped>
@import '@/assets/views/add-recipe-view.css';

.add-recipe-view {
  padding-top: 2rem;
  padding-bottom: 4rem;
}

.view-title {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #333;
  font-weight: 500;
}
</style>
