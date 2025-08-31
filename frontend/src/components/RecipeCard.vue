<template>
  <v-card class="mx-auto d-flex flex-column fill-height" flat border>
    <v-img
      :src="imageSrc"
      height="200px"
      cover
    ></v-img>

    <div class="d-flex flex-column flex-grow-1 pa-4">
      <v-card-title class="pa-0 mb-2 text-body-1 font-weight-medium">
        {{ recipe.name }}
      </v-card-title>

      <div class="mb-3">
        <v-chip
          v-for="(tag, index) in recipe.tags"
          :key="index"
          size="small"
          class="mr-1 mb-1"
          label
          :color="getTagColor(tag)"
          variant="tonal"
          @click.stop="handleTagClick(tag)"
          style="cursor: pointer;"
        >
          {{ tag }}
        </v-chip>
      </div>

      <v-card-text class="pa-0 mb-2 text-body-2 text-medium-emphasis flex-grow-1">
        <div class="ingredients-section">
          <div class="ingredients-title">
            <v-icon icon="mdi-food-variant" color="primary" size="small" class="mr-1"></v-icon>
            <strong class="text-body-2 font-weight-medium">主要食材</strong>
          </div>
          <ul class="ingredient-list">
            <li v-for="(ingredient, index) in recipe.ingredients.slice(0, 6)" :key="index">
              <span class="ingredient-name">{{ ingredient.name }}</span>
              <span class="ingredient-quantity">{{ ingredient.quantity }}</span>
            </li>
          </ul>
        </div>
      </v-card-text>

      <v-divider class="my-2"></v-divider>

      <v-card-actions class="pa-0">
        <v-btn
          :to="`/recipes/${recipe.id}`" 
          color="grey-darken-1"
          variant="text"
          size="small"
        >
          查看详情
          <v-icon right icon="mdi-chevron-right"></v-icon>
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn icon="mdi-pencil" size="small" variant="text" color="orange-lighten-2" @click.stop="editRecipe"></v-btn>
        <v-btn icon="mdi-delete" size="small" variant="text" color="red-lighten-2" @click.stop="deleteRecipe"></v-btn>
        <v-btn 
          icon="mdi-silverware-fork-knife"
          size="small"
          variant="text"
          :color="todayMenu.hasRecipeInWorkingMenu(recipe.id) ? 'grey' : 'green-lighten-2'"
          :disabled="todayMenu.hasRecipeInWorkingMenu(recipe.id)"
          @click.stop="addToToday"
          title="添加到今日菜单"
        ></v-btn>
      </v-card-actions>
    </div>
  </v-card>

  <!-- Reusable Delete Confirmation Dialog -->
  <DeleteConfirmation
    v-model="showDeleteDialog"
    :recipe="props.recipe"
    :loading="isDeleting"
    @confirm="handleConfirmDelete"
  />
</template>

<script setup>
import { ref, onMounted } from 'vue'; // Import ref
import { useRouter } from 'vue-router';
import { useTodayMenuStore } from '@/stores/todayMenu';
import api, { getRecipeImage } from '@/services/api';
import DeleteConfirmation from '@/components/DeleteConfirmation.vue'; // Import the component

// --- State ---
const showDeleteDialog = ref(false);
const isDeleting = ref(false);
const imageSrc = ref(require('@/assets/recipe_default_image.png'));

const props = defineProps({
  recipe: {
    type: Object,
    required: true,
    default: () => ({
        id: 0,
        name: '无标题',
        image: '',
        tags: [],
        ingredients: '无'
    })
  },
  // Add snackbar prop to accept the v-model value from the parent
  snackbar: {
    type: Object,
    required: false // Or true if the parent always provides it
  }
});

// Emits updated to include tagClicked
const emit = defineEmits(['recipeDeleted', 'update:snackbar', 'tagClicked']);
const router = useRouter();
const todayMenu = useTodayMenuStore();

onMounted(async () => {
  try {
    const imageUrl = await getRecipeImage(props.recipe.id);
    imageSrc.value = imageUrl;
  } catch (error) {
    console.error(`Failed to load image for recipe ${props.recipe.id}`);
  }
});

// --- Methods ---
const getTagColor = (tag) => {
  // Example logic to assign colors to tags
  if (['简单', '清淡'].includes(tag)) return 'green';
  if (['中等', '家常菜', '咸鲜', '酸甜', '烘培', '西餐'].includes(tag)) return 'blue';
  if (['困难', '川菜', '湘菜', '闽菜'].includes(tag)) return 'orange';
  if (['麻辣', '香辣', '热菜'].includes(tag)) return 'red';
  return 'grey'; // Default color
};

const editRecipe = () => {
  // Navigate to the edit page for this recipe
  router.push({ name: 'edit-recipe', params: { id: props.recipe.id } });
};

// --- Delete Logic ---
const deleteRecipe = () => {
  // Show the confirmation dialog instead of window.confirm
  showDeleteDialog.value = true;
};

const handleConfirmDelete = async () => {
  isDeleting.value = true;
  try {
    await api.deleteRecipe(props.recipe.id);
    // Emit an event to notify the parent component (HomeView)
    emit('recipeDeleted', props.recipe.id);
    showDeleteDialog.value = false; // Close dialog on success
    // Optionally show a local success message or rely on parent's snackbar
  } catch (error) {
    console.error(`Failed to delete recipe ${props.recipe.id}:`, error);
    // Emit snackbar update on error
    emit('update:snackbar', {
      show: true,
      text: `删除菜谱 "${props.recipe.name}" 失败: ${error.response?.data?.description || error.message || '请稍后再试'}`,
      color: 'error',
      timeout: 3000 // Or use a default timeout from parent
    });
    showDeleteDialog.value = false; // Close dialog even on error
  } finally {
    isDeleting.value = false;
  }
};

// --- Tag Click Logic ---
const handleTagClick = (tag) => {
  emit('tagClicked', tag);
};

// --- Add to Today Logic ---
const addToToday = () => {
  // Use the correct action from the store
  if (todayMenu.addRecipeToTodayWorkingMenu(props.recipe)) {
    // If the recipe was successfully added (wasn't already in the working menu)
    emit('update:snackbar', {
      show: true,
      text: `菜谱 "${props.recipe.name}" 已添加到今日菜单`,
      color: 'success'
    });
  }
};
</script>

<style scoped>
@import '@/assets/components/recipe-card.css';
</style>
