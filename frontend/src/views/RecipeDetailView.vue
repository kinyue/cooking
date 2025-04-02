<template>
  <v-container>
    <!-- Main content card - only render when recipe data is loaded and not loading -->
    <v-row v-if="recipe && !loading" justify="center">
      <v-col cols="12" md="8">
        <v-card>
          <v-img
            src="https://picsum.photos/800/400?random"
            height="400"
            cover
          ></v-img>

          <v-card-title class="text-h4 font-weight-bold">
            {{ recipe.name }}
          </v-card-title>

          <v-card-subtitle class="mt-2">
            {{ recipe.description }}
          </v-card-subtitle>

          <v-card-text>
            <h3 class="text-h5 font-weight-bold mt-4">主要食材</h3>
            <ul>
              <li v-for="(ingredient, index) in recipe.ingredients" :key="index">
                {{ ingredient.name }} - {{ ingredient.quantity }}
              </li>
            </ul>

            <h3 class="text-h5 font-weight-bold mt-4">烹饪步骤</h3>
            <ol>
              <li v-for="(step, index) in recipe.instructions" :key="index">
                {{ step }}
              </li>
            </ol>

            <v-chip-group class="mt-4">
              <v-chip
                v-for="tag in recipe.tags"
                :key="tag"
                label
                class="ma-1"
              >
                {{ tag }}
              </v-chip>
            </v-chip-group>
          </v-card-text>

          <v-card-actions class="justify-end">
            <v-btn color="primary" @click="$router.back()">
              返回
            </v-btn>
            <v-btn color="primary" @click="editRecipe">
              编辑
            </v-btn>
            <v-btn color="error" @click="deleteRecipe">
              删除
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Loading indicator -->
    <v-row v-if="loading" justify="center">
      <v-col cols="12" class="text-center">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
      </v-col>
    </v-row>

    <!-- Error message -->
    <v-row v-else-if="error" justify="center">
      <v-col cols="12">
        <v-alert type="error" text="加载菜谱详情失败，请稍后重试。" :value="true"></v-alert>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
// import { ref, onMounted } from 'vue'; // Keep ref/onMounted commented if not used directly here
import { useRoute, useRouter } from 'vue-router';
// Import the named export getRecipeById
import { getRecipeById } from '@/services/api';

export default {
  name: 'RecipeDetailView',
  data() {
    return {
      recipe: null,
      loading: false,
      error: null,
    };
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    return { route, router };
  },
  mounted() {
    this.fetchRecipeDetails();
  },
  watch: {
    '$route.params.id': 'fetchRecipeDetails'
  },
  methods: {
    async fetchRecipeDetails() {
      this.loading = true;
      this.error = null;
      try {
        const recipeId = this.route.params.id;
        const response = await getRecipeById(recipeId);
        this.recipe = response.data;
      } catch (error) {
        console.error('Failed to fetch recipe details:', error);
        this.error = error;
      } finally {
        this.loading = false;
      }
    },
    editRecipe() {
      // Navigate to edit recipe view
      this.router.push({ name: 'edit-recipe', params: { id: this.recipe.id } });
    },
    deleteRecipe() {
      // TODO: Implement delete recipe logic
      console.log('Delete recipe clicked');
    },
  },
};
</script>

<style scoped>
@import '@/assets/views/recipe-detail-view.css';
</style>
