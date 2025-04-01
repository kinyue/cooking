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
// import api from '@/services/api'; // Import your API service

// --- State ---
const recommendCount = ref(12); // Default recommendation count
const countOptions = ref([4, 8, 12, 16, 20, 24]); // Options for the dropdown
const recipes = ref([]); // Array to hold recipe data
const loading = ref(false); // Loading state indicator
const error = ref(null); // Error state holder

// --- Mock Data (Replace with API call) ---
const mockRecipes = [
  // Add 12 sample recipes matching the design structure
  // Example:
  { id: 1, name: '清蒸鲈鱼', image: 'https://via.placeholder.com/300x200/CCCCCC/969696?text=Recipe+Image', tags: ['中等', '粤菜', '清淡'], ingredients: '鲈鱼, 姜, 葱, 蒸鱼豉油, 香菜' },
  { id: 2, name: '番茄炒蛋', image: 'https://via.placeholder.com/300x200/CCCCCC/969696?text=Recipe+Image', tags: ['简单', '家常菜', '酸甜'], ingredients: '西红柿, 鸡蛋, 葱, 糖, 盐' },
  { id: 3, name: '红烧排骨', image: 'https://via.placeholder.com/300x200/CCCCCC/969696?text=Recipe+Image', tags: ['中等', '家常菜', '咸鲜'], ingredients: '排骨, 生姜, 酱油, 料酒, 冰糖' },
  { id: 4, name: '糖醋里脊', image: 'https://via.placeholder.com/300x200/CCCCCC/969696?text=Recipe+Image', tags: ['中等', '热菜', '酸甜'], ingredients: '猪里脊, 胡萝卜, 青椒, 白糖, 醋' },
  { id: 5, name: '蛋黄酥', image: 'https://via.placeholder.com/300x200/CCCCCC/969696?text=Recipe+Image', tags: ['中等', '烘培', '咸鲜'], ingredients: '低筋面粉, 咸蛋黄, 豆沙, 黄油, 细砂糖' },
  { id: 6, name: '小龙虾', image: 'https://via.placeholder.com/300x200/CCCCCC/969696?text=Recipe+Image', tags: ['简单', '湘菜', '麻辣'], ingredients: '小龙虾, 啤酒, 麻辣香锅料, 蒜, 姜' },
  { id: 7, name: '佛跳墙', image: 'https://via.placeholder.com/300x200/CCCCCC/969696?text=Recipe+Image', tags: ['困难', '闽菜', '咸鲜'], ingredients: '鱼翅, 鲍鱼, 海参, 花胶, 瑶柱' },
  { id: 8, name: '香草烤鸡', image: 'https://via.placeholder.com/300x200/CCCCCC/969696?text=Recipe+Image', tags: ['中等', '西餐', '咸鲜'], ingredients: '整鸡, 迷迭香, 黄油, 柠檬, 大蒜' },
  { id: 9, name: '宫保鸡丁', image: 'https://via.placeholder.com/300x200/CCCCCC/969696?text=Recipe+Image', tags: ['中等', '川菜', '香辣'], ingredients: '鸡胸肉, 花生, 干辣椒, 葱, 蒜' },
  { id: 10, name: '麻婆豆腐', image: 'https://via.placeholder.com/300x200/CCCCCC/969696?text=Recipe+Image', tags: ['简单', '川菜', '麻辣'], ingredients: '豆腐, 肉末, 豆瓣酱, 花椒, 葱' },
  { id: 11, name: '水煮鱼', image: 'https://via.placeholder.com/300x200/CCCCCC/969696?text=Recipe+Image', tags: ['中等', '川菜', '麻辣'], ingredients: '鱼片, 豆芽, 辣椒, 花椒, 葱' },
  { id: 12, name: '爆炒肥肠', image: 'https://via.placeholder.com/300x200/CCCCCC/969696?text=Recipe+Image', tags: ['困难', '川菜', '香辣'], ingredients: '肥肠, 青椒, 红椒, 干辣椒, 蒜' },
];

// --- Methods ---
const fetchRecipes = async (count) => {
  loading.value = true;
  error.value = null;
  try {
    // --- Use Mock Data (Comment out API call) ---
     await new Promise(resolve => setTimeout(resolve, 500)); // Simulate network delay
     recipes.value = mockRecipes.slice(0, count);
    // --- OR Use API Call (Uncomment below and comment mock data) ---
    // const data = await api.getRecipes({ count: count }); // Assuming API supports count param
    // recipes.value = data; // Adjust based on actual API response structure

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
