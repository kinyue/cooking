<template>
  <v-container fluid class="pa-5">
    <v-row align="center" class="mb-4">
      <v-col cols="12" sm="auto">
        <h1 class="text-h5 font-weight-medium">推荐菜谱</h1>
      </v-col>
      <v-spacer></v-spacer>
      <v-col cols="6" sm="3" md="2">
        <v-select
          v-model="recommendCount"
          :items="countOptions"
          label="推荐数量"
          density="compact"
          variant="outlined"
          hide-details
        ></v-select>
      </v-col>
      <v-col cols="6" sm="auto">
        <v-btn color="primary" @click="startRecommendation" size="large">
          <v-icon left icon="mdi-play-circle-outline" class="mr-1"></v-icon>
          开始推荐
        </v-btn>
      </v-col>
    </v-row>

    <v-row>
      <v-col
        v-for="recipe in recipes"
        :key="recipe.id"
        cols="12"
        sm="6"
        md="4"
        lg="3"
      >
        <RecipeCard :recipe="recipe" />
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
</template>

<script setup>
import { ref, onMounted } from 'vue';
import RecipeCard from '@/components/RecipeCard.vue'; // Import the RecipeCard component
import api from '@/services/api'; // Import your API service

// --- State ---
const recommendCount = ref(12); // Default recommendation count
const countOptions = ref([4, 8, 12, 16, 20, 24]); // Options for the dropdown
const recipes = ref([]); // Array to hold recipe data
const loading = ref(false); // Loading state indicator
const error = ref(null); // Error state holder


// --- Methods ---
const fetchRecipes = async (count) => {
  loading.value = true;
  error.value = null;
  try {
    // --- Use Mock Data (Comment out API call) ---
     // await new Promise(resolve => setTimeout(resolve, 500)); // Simulate network delay
     // recipes.value = mockRecipes.slice(0, count);
    // --- OR Use API Call (Uncomment below and comment mock data) ---
    const data = await api.getRecipes({ count: count }); // Assuming API supports count param
    recipes.value = data.data; // Adjust based on actual API response structure

  } catch (err) {
    console.error("Failed to fetch recipes:", err);
    error.value = err;
    recipes.value = []; // Clear recipes on error
  } finally {
    loading.value = false;
  }
};

const startRecommendation = () => {
  console.log(`Starting recommendation with count: ${recommendCount.value}`);
  fetchRecipes(recommendCount.value); // Re-fetch recipes based on selected count
};

// --- Lifecycle Hooks ---
onMounted(() => {
  fetchRecipes(recommendCount.value); // Fetch initial recipes when component mounts
});

</script>

<style scoped>
@import '@/assets/views/home-view.css';
</style>
