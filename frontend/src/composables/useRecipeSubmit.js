import { ref } from 'vue';
import { createRecipe, uploadRecipeImage } from '@/services/api';

/**
 * Composable function to handle the logic of submitting a new recipe,
 * including creating the recipe data and uploading an optional image.
 *
 * @returns {object} An object containing:
 *   - isSubmitting: A ref boolean indicating if the submission is in progress.
 *   - error: A ref string containing any error message during submission.
 *   - submitRecipe: An async function to execute the submission process.
 */
export function useRecipeSubmit() {
  const isSubmitting = ref(false);
  const error = ref(null); // Store error message

  /**
   * Submits the recipe data and optional image file.
   * @param {object} payload - The payload object.
   * @param {object} payload.recipeData - The recipe data object.
   * @param {File|null} payload.imageFile - The image file object, or null.
   * @returns {Promise<number|null>} A promise that resolves with the new recipe ID if successful, otherwise null.
   */
  const submitRecipe = async ({ recipeData, imageFile }) => {
    isSubmitting.value = true;
    error.value = null; // Reset error before new submission
    let newRecipeId = null;

    try {
      // Step 1: Create the recipe text data
      const createdRecipeResponse = await createRecipe({ recipeData: recipeData });

      newRecipeId = createdRecipeResponse?.data?.id;

      if (!newRecipeId) {
        console.error("useRecipeSubmit: Failed to extract newRecipeId from response:", JSON.stringify(createdRecipeResponse, null, 2)); // Keep error log
        throw new Error('创建菜谱失败，服务器未返回有效的菜谱ID。');
      }

      // Step 2: If an image file was provided AND we have a valid ID, upload it
      if (imageFile && newRecipeId) {
        try {
          await uploadRecipeImage(newRecipeId, imageFile);
        } catch (uploadError) {
          console.error('useRecipeSubmit: 图片上传失败:', uploadError); // Keep error log
          // Throw a combined error message
          throw new Error(`菜谱已创建 (ID: ${newRecipeId})，但图片上传失败: ${uploadError.message || '未知错误'}`);
        }
      }

      return newRecipeId; // Return the ID on full success

    } catch (err) {
      console.error('useRecipeSubmit: 创建/上传过程中出错:', err); // Keep error log
      error.value = err.message || '提交过程中发生未知错误。';
      return null; // Indicate failure by returning null
    } finally {
      isSubmitting.value = false;
    }
  };

  return {
    isSubmitting,
    error,
    submitRecipe,
  };
}
