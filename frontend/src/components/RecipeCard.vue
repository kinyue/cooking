<template>
  <v-card class="mx-auto d-flex flex-column fill-height" flat border>
    <v-img
      :src="recipe.image || 'https://via.placeholder.com/300x200/E0E0E0/BDBDBD?text=No+Image'"
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
        <v-btn icon="mdi-plus-box" size="small" variant="text" color="green-lighten-2" @click.stop="addToToday"></v-btn> 
      </v-card-actions>
    </div>
  </v-card>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'; // Import defineEmits
import { useRouter } from 'vue-router'; // Import useRouter
import api from '@/services/api'; // Import api service

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
  }
});

const emit = defineEmits(['recipeDeleted', 'addToTodayClicked']); // Define emits
const router = useRouter(); // Get router instance

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

const deleteRecipe = async () => {
  // Confirm deletion with the user
  if (window.confirm(`确定要删除菜谱 "${props.recipe.name}" 吗？`)) {
    try {
      await api.deleteRecipe(props.recipe.id);
      // Emit an event to notify the parent component (HomeView)
      emit('recipeDeleted', props.recipe.id);
      // Optionally show a local success message or rely on parent's snackbar
    } catch (error) {
      console.error(`Failed to delete recipe ${props.recipe.id}:`, error);
      // Optionally show an error message to the user
      alert(`删除失败: ${error.response?.data?.description || error.message || '请稍后再试'}`);
    }
  }
};

// Method to handle adding the recipe to today's menu (placeholder)
const addToToday = () => {
  console.log('Add to today clicked for recipe:', props.recipe.id);
  // Emit an event to notify the parent component
  emit('addToTodayClicked', props.recipe.id);
};
</script>

<style scoped>
@import '@/assets/components/recipe-card.css';
</style>
