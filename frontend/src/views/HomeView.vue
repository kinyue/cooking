<!-- frontend/src/views/HomeView.vue -->
<!-- Page component to display the list of recipes -->
<template>
  <v-container>
    <h1 class="mb-4">推荐菜谱</h1>

    <!-- Loading Indicator -->
    <v-row v-if="loading">
      <v-col cols="12" class="text-center">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
        <p>加载中...</p>
      </v-col>
    </v-row>

    <!-- Error Message -->
    <v-row v-else-if="error">
       <v-col cols="12">
        <v-alert type="error" prominent border="start">
          加载菜谱时出错: {{ error.message || '未知错误' }}
        </v-alert>
      </v-col>
    </v-row>

    <!-- Recipe List -->
    <v-row v-else>
      <v-col
        v-for="recipe in recipes"
        :key="recipe.id"
        cols="12"
        sm="6"
        md="4"
        lg="3"
      >
        <!-- RecipeCard component will go here -->
        <!-- For now, just display basic info -->
        <v-card>
          <v-img
            :src="recipe.image_url || 'https://via.placeholder.com/300x200?text=No+Image'"
            height="200px"
            cover
          ></v-img>
          <v-card-title>{{ recipe.name }}</v-card-title>
          <v-card-subtitle class="pb-2">
             <!-- Display tags using v-chip -->
             <v-chip v-if="recipe.difficulty" size="small" class="mr-1 mb-1">{{ recipe.difficulty }}</v-chip>
             <v-chip v-if="recipe.cuisine" size="small" class="mr-1 mb-1">{{ recipe.cuisine }}</v-chip>
             <v-chip v-for="tag in recipe.tags" :key="tag" size="small" class="mr-1 mb-1">{{ tag }}</v-chip>
          </v-card-subtitle>
           <v-card-text>
             <!-- Basic ingredients preview -->
             <p class="text-caption">主要食材: {{ previewIngredients(recipe.ingredients) }}</p>
           </v-card-text>
          <v-card-actions>
            <v-btn color="primary" variant="text" :to="{ name: 'recipe-detail', params: { id: recipe.id } }">
              查看详情
            </v-btn>
            <v-spacer></v-spacer>
            <!-- Placeholder for Edit/Delete/Add to Menu buttons -->
             <v-btn icon="mdi-pencil" size="small" variant="text" :to="{ name: 'edit-recipe', params: { id: recipe.id } }"></v-btn>
             <v-btn icon="mdi-delete" size="small" variant="text" @click="handleDelete(recipe.id)"></v-btn>
             <v-btn icon="mdi-plus-box" size="small" variant="text" @click="addToMenu(recipe)"></v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
       <v-col v-if="recipes.length === 0 && !loading" cols="12">
         <p>暂无菜谱。</p>
         <v-btn color="primary" :to="{ name: 'add-recipe' }">添加第一个菜谱</v-btn>
       </v-col>
    </v-row>

     <!-- TODO: Add filtering controls -->
     <!-- TODO: Add "Add Recipe" button (maybe in AppHeader) -->
     <!-- TODO: Add "Today's Menu" functionality -->
     <!-- TODO: Implement Delete confirmation dialog -->

  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getRecipes, deleteRecipe as apiDeleteRecipe } from '@/services/api'; // Use @ alias
import { useRouter } from 'vue-router';

const recipes = ref([]);
const loading = ref(true);
const error = ref(null);
const router = useRouter();

// Fetch recipes when the component is mounted
onMounted(async () => {
  try {
    loading.value = true;
    error.value = null;
    const response = await getRecipes();
    // Assuming the API returns { data: [...] }
    recipes.value = response.data.data || [];
  } catch (err) {
    console.error("Failed to fetch recipes:", err);
    error.value = err.response?.data || err; // Store error info
  } finally {
    loading.value = false;
  }
});

// Helper function for previewing ingredients
const previewIngredients = (ingredients) => {
  if (!ingredients || !Array.isArray(ingredients)) return 'N/A';
  return ingredients.slice(0, 3).map(ing => ing.name).join(', ') + (ingredients.length > 3 ? '...' : '');
};

// Placeholder for delete action
const handleDelete = async (id) => {
  // Implement confirmation dialog first
  if (confirm(`确定要删除 ID 为 ${id} 的菜谱吗？`)) {
    try {
      await apiDeleteRecipe(id);
      // Remove the recipe from the local list
      recipes.value = recipes.value.filter(recipe => recipe.id !== id);
      // Optionally show a success notification
    } catch (err) {
      console.error(`Failed to delete recipe ${id}:`, err);
      // Show an error notification to the user
      alert(`删除失败: ${err.response?.data?.message || err.message}`);
    }
  }
};

// Placeholder for adding to today's menu
const addToMenu = (recipe) => {
  console.log('Add to menu:', recipe.name);
  // Implement logic to add to a temporary list or state management store
  alert(`${recipe.name} 已添加到今日菜单 (功能待实现)`);
};

</script>

<style scoped>
/* Add any specific styles for HomeView here */
.v-card-actions .v-btn {
  color: rgba(0, 0, 0, 0.6);
}
</style>
