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
import { ref, onMounted } from 'vue';
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

// --- Methods ---
const fetchRecipes = async () => {
  loading.value = true;
  error.value = null;
  try {
    const data = await api.getRecipes(); 
    recipes.value = data.data; 

  } catch (err) {
    console.error("Failed to fetch recipes:", err);
    error.value = err;
    recipes.value = [];
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
    await fetchRecipes();
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
const handleRecipeDeleted = (recipeId) => {
  const index = recipes.value.findIndex(r => r.id === recipeId);
  if (index !== -1) {
    const deletedRecipeName = recipes.value[index].name;
    recipes.value.splice(index, 1);
    snackbar.value = {
      show: true,
      text: `菜谱 "${deletedRecipeName}" 已删除`,
      color: 'success'
    };
  }
};

// Handler for canceling the add recipe dialog
const handleCancelAdd = () => {
  showAddDialog.value = false;
};

// --- Lifecycle Hooks ---
onMounted(() => {
  fetchRecipes();
  
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
</style>
