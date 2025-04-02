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

          <v-card-subtitle class="mt-2 text-body-1">
            {{ recipe.description }}
          </v-card-subtitle>

          <v-card-text>
            <!-- Recipe Info Grid -->
            <v-row class="mt-2">
              <v-col cols="12" sm="6" md="4">
                <v-card variant="flat" class="pa-2 text-center bg-grey-lighten-4">
                  <v-icon icon="mdi-calendar-clock" size="large" class="mb-2" color="primary"></v-icon>
                  <div class="text-caption text-medium-emphasis mb-1">准备时间</div>
                  <div class="text-subtitle-1 font-weight-medium">{{ recipe.prep_time_minutes || '未设置' }} 分钟</div>
                </v-card>
              </v-col>

              <v-col cols="12" sm="6" md="4">
                <v-card variant="flat" class="pa-2 text-center bg-grey-lighten-4">
                  <v-icon icon="mdi-pot-steam" size="large" class="mb-2" color="primary"></v-icon>
                  <div class="text-caption text-medium-emphasis mb-1">烹饪时间</div>
                  <div class="text-subtitle-1 font-weight-medium">{{ recipe.cook_time_minutes || '未设置' }} 分钟</div>
                </v-card>
              </v-col>

              <v-col cols="12" sm="6" md="4">
                <v-card variant="flat" class="pa-2 text-center bg-grey-lighten-4">
                  <v-icon icon="mdi-silverware-variant" size="large" class="mb-2" color="primary"></v-icon>
                  <div class="text-caption text-medium-emphasis mb-1">份量</div>
                  <div class="text-subtitle-1 font-weight-medium">{{ recipe.servings || '未设置' }} 份</div>
                </v-card>
              </v-col>

              <v-col cols="12" sm="6" md="4">
                <v-card variant="flat" class="pa-2 text-center bg-grey-lighten-4">
                  <v-icon icon="mdi-speedometer" size="large" class="mb-2" color="primary"></v-icon>
                  <div class="text-caption text-medium-emphasis mb-1">难度</div>
                  <div class="text-subtitle-1 font-weight-medium">{{ recipe.difficulty || '未设置' }}</div>
                </v-card>
              </v-col>

              <v-col cols="12" sm="6" md="4">
                <v-card variant="flat" class="pa-2 text-center bg-grey-lighten-4">
                  <v-icon icon="mdi-food-variant" size="large" class="mb-2" color="primary"></v-icon>
                  <div class="text-caption text-medium-emphasis mb-1">菜系</div>
                  <div class="text-subtitle-1 font-weight-medium">{{ recipe.cuisine || '未设置' }}</div>
                </v-card>
              </v-col>
            </v-row>

            <!-- Tags -->
            <v-chip-group class="mt-6">
              <v-chip v-for="tag in recipe.tags" :key="tag" label color="primary" variant="flat" class="ma-1">
                {{ tag }}
              </v-chip>
            </v-chip-group>

            <!-- Ingredients Section -->
            <v-divider class="my-6"></v-divider>
            <h3 class="text-h5 font-weight-medium mb-4">
              <v-icon icon="mdi-food-apple" color="primary" class="mr-2"></v-icon>主要食材
            </h3>
            <v-list>
              <v-list-item v-for="(ingredient, index) in recipe.ingredients" :key="index" density="compact">
                <v-list-item-title>
                  {{ ingredient.name }} - {{ ingredient.quantity }}
                </v-list-item-title>
              </v-list-item>
            </v-list>

            <!-- Instructions Section -->
            <v-divider class="my-6"></v-divider>
            <h3 class="text-h5 font-weight-medium mb-4">
              <v-icon icon="mdi-chef-hat" color="primary" class="mr-2"></v-icon>烹饪步骤
            </h3>
            <v-timeline density="comfortable" class="mt-4">
              <v-timeline-item v-for="(step, index) in recipe.instructions" :key="index" 
                :dot-color="'primary'"
                size="small"
                class="pb-4"
              >
                <template v-slot:title>
                  <span class="text-h6 font-weight-regular">步骤 {{ index + 1 }}</span>
                </template>
                <div class="text-body-1 mt-1">{{ step }}</div>
              </v-timeline-item>
            </v-timeline>
          </v-card-text>

          <!-- Action Buttons -->
          <v-divider></v-divider>
          <v-card-actions class="pa-4">
            <v-btn 
              color="grey-darken-1" 
              variant="text" 
              @click="$router.push('/')" 
              prepend-icon="mdi-arrow-left"
            >
              返回
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn icon="mdi-pencil" size="small" variant="text" color="orange-lighten-2" @click.stop="editRecipe"></v-btn>
            <v-btn icon="mdi-delete" size="small" variant="text" color="red-lighten-2" @click.stop="deleteRecipe"></v-btn>
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
