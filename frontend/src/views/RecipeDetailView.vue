<template>
  <v-container fluid class="pa-5">
    <!-- Main content card - only render when recipe data is loaded and not loading -->
    <v-row v-if="recipe && !loading" justify="center">
      <v-col cols="12" md="8">
        <v-card class="elevation-2">
          <v-img src="https://picsum.photos/800/400?random" height="400" cover></v-img>

          <v-card-title class="text-h4 font-weight-medium">
            {{ recipe.name }}
          </v-card-title>

          <v-card-subtitle class="mt-2">
            {{ recipe.description }}
          </v-card-subtitle>

          <v-card-text>
            <h3 class="text-h5 font-weight-medium mt-6 mb-3">主要食材</h3>
            <v-list>
              <v-list-item v-for="(ingredient, index) in recipe.ingredients" :key="index" density="compact">
                <v-list-item-title>
                  {{ ingredient.name }} - {{ ingredient.quantity }}
                </v-list-item-title>
              </v-list-item>
            </v-list>

            <h3 class="text-h5 font-weight-medium mt-6 mb-3">烹饪步骤</h3>
            <v-timeline density="compact">
              <v-timeline-item v-for="(step, index) in recipe.instructions" :key="index" :dot-color="'primary'"
                size="small">
                {{ step }}
              </v-timeline-item>
            </v-timeline>

            <v-chip-group class="mt-6">
              <v-chip v-for="tag in recipe.tags" :key="tag" label class="ma-1">
                {{ tag }}
              </v-chip>
            </v-chip-group>
          </v-card-text>

          <v-divider class="my-3"></v-divider>
          <v-card-actions class="pa-4">
            <v-btn color="grey-darken-1" variant="text" size="small" @click="$router.back()" prepend-icon="mdi-arrow-left">
              返回
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn icon="mdi-pencil" size="small" variant="text" color="orange-lighten-2"
              @click.stop="editRecipe"></v-btn>
            <v-btn icon="mdi-delete" size="small" variant="text" color="orange-lighten-2"
              @click.stop="deleteRecipe"></v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Loading indicator -->
    <v-row v-if="loading" justify="center" align="center" style="min-height: 200px;">
      <v-col cols="12" class="text-center">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
        <p class="mt-2 text-medium-emphasis">加载中...</p>
      </v-col>
    </v-row>

    <!-- Error message -->
    <v-row v-else-if="error" justify="center">
      <v-col cols="12" md="8">
        <v-alert type="error" variant="tonal" title="加载失败" text="加载菜谱详情失败，请稍后重试。" class="mb-4"></v-alert>
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
