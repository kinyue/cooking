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
            <v-btn 
              icon="mdi-plus-box" 
              size="small" 
              variant="text" 
              :color="todayMenu.hasRecipe(recipe.id) ? 'grey' : 'green-lighten-2'" 
              :disabled="todayMenu.hasRecipe(recipe.id)"
              @click.stop="addToToday"
            ></v-btn>
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

  <!-- Use the reusable Delete Confirmation Dialog -->
  <DeleteConfirmation
    v-model="dialog.show"
    :recipe="recipe"
    :loading="dialog.loading"
    @confirm="confirmDelete"
  />

  <!-- Error Snackbar -->
  <v-snackbar
    v-model="snackbar.show"
    :color="snackbar.color"
    :timeout="snackbar.timeout"
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

<script>
import { useRoute, useRouter } from 'vue-router';
import { getRecipeById, deleteRecipe } from '@/services/api';
import DeleteConfirmation from '@/components/DeleteConfirmation.vue'; // Import the component
import { useTodayMenuStore } from '@/stores/todayMenu'; // Import the store


export default {
  name: 'RecipeDetailView',
  // Define props to accept the 'id' from the router
  props: {
    id: {
      type: [String, Number], // Accept both string (from URL) and number
      required: true
    }
  },
  components: { // Register the component
    DeleteConfirmation,
  },
  data() {
    return {
      recipe: null,
      loading: false,
      error: null,
      dialog: {
        show: false,
        loading: false
      },
      snackbar: {
        show: false,
        text: '',
        color: 'error',
        timeout: 3000
      }
    };
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const todayMenu = useTodayMenuStore(); // Instantiate the store inside setup
    return { route, router, todayMenu }; // Return todayMenu
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
        // Access id directly via props now
        const response = await getRecipeById(this.id); 
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
      this.dialog.show = true;
    },
    async confirmDelete() {
      try {
        this.dialog.loading = true;
        const recipeName = this.recipe.name;
        await deleteRecipe(this.recipe.id);
        this.dialog.show = false;
        // On success, navigate to home with query parameter
        this.router.push({
          name: 'home',
          query: { deletedRecipe: recipeName }
        });
      } catch (error) {
        console.error('Failed to delete recipe:', error);
        this.dialog.show = false;
        // Show error snackbar in current page
        this.snackbar = {
          show: true,
          text: `删除菜谱失败: ${error.message || '请稍后重试'}`,
          color: 'error',
          timeout: 3000
        };
      } finally {
        this.dialog.loading = false;
      }
    },
    // Method to add the current recipe to today's menu
    addToToday() {
      if (!this.recipe) return; // Guard against missing recipe data

      // Access store via this.todayMenu now
      if (this.todayMenu.addRecipe(this.recipe)) { 
        // If the recipe was successfully added (wasn't already in the menu)
        this.snackbar = {
          show: true,
          text: `菜谱 "${this.recipe.name}" 已添加到今日菜单`,
          color: 'success',
          timeout: 3000
        };
        // Optionally, force re-render if button state doesn't update automatically
        // this.$forceUpdate(); 
      } else {
        // Handle case where recipe might already be in the menu (optional feedback)
        this.snackbar = {
          show: true,
          text: `菜谱 "${this.recipe.name}" 已在今日菜单中`,
          color: 'info', // Use info color for existing items
          timeout: 3000
        };
      }
    },
  },
};
</script>

<style scoped>
@import '@/assets/views/recipe-detail-view.css';
</style>
