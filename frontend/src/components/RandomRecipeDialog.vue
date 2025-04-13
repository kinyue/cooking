<template>
  <v-dialog v-model="dialogVisible" max-width="400px" persistent class="random-recipe-dialog">
    <v-card>
      <v-card-title class="d-flex justify-space-between align-center">
        <span>随机推荐</span>
        <v-btn icon @click="closeDialog" :disabled="isLoading">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-card-text>
        <v-progress-circular
          v-if="isLoading"
          indeterminate
          color="primary"
          class="loading-indicator"
        ></v-progress-circular>

        <div v-else-if="currentRecipe" class="recipe-display-area">
          <!-- Display the single recipe card -->
          <div class="mini-recipe-card-container">
             <MiniRecipeCard :recipe="currentRecipe" />
          </div>

          <!-- Action Buttons -->
          <div class="card-actions">
            <v-btn
              color="error"
              @click="handleNext"
              :disabled="isLoading"
              variant="outlined"
              density="comfortable"
            >
              <v-icon>mdi-dice-5-outline</v-icon>
              换一个
            </v-btn>
            <v-btn
              color="primary"
              @click="handleAddToMenu"
              :disabled="isLoading"
              variant="elevated"
              density="comfortable"
            >
              <v-icon>mdi-silverware-fork-knife</v-icon>
              加入菜单
            </v-btn>
          </div>
        </div>

        <!-- Error/No Recipe State -->
        <div v-else-if="!isLoading && error" class="finished-state">
          <v-icon size="64" color="warning" class="mb-4">mdi-alert-circle-outline</v-icon>
          <p>{{ error }}</p>
          <v-btn color="primary" @click="reRoll">
             <v-icon left>mdi-refresh</v-icon>
             重试
          </v-btn>
        </div>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import { fetchRandomRecipes } from '@/services/api';
import { useTodayMenuStore } from '@/stores/todayMenu';
import MiniRecipeCard from '@/components/MiniRecipeCard.vue';

const props = defineProps({
  modelValue: Boolean,
});

const emit = defineEmits(['update:modelValue']);

const todayMenuStore = useTodayMenuStore();

const dialogVisible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value),
});

const currentRecipe = ref(null); // Store only one recipe
const isLoading = ref(false);
const error = ref(null);

// Simplified function to load a single random recipe
async function loadSingleRecipe() {
  isLoading.value = true;
  error.value = null;
  currentRecipe.value = null; // Clear previous recipe

  try {
    // Fetch only one recipe
    const recipes = await fetchRandomRecipes(1); 
    if (recipes && recipes.length > 0) {
      currentRecipe.value = recipes[0];
    } else {
      error.value = "未找到菜谱";
    }
  } catch (err) {
    console.error("Failed to load random recipe:", err);
    error.value = "加载随机菜谱失败";
  } finally {
    isLoading.value = false;
  }
}

// Handle "Next" button click - load a new recipe
function handleNext() {
  if (isLoading.value) return;
  loadSingleRecipe();
}

// Handle "Add to Menu" button click - add current and load a new one
function handleAddToMenu() {
  if (isLoading.value || !currentRecipe.value) return;
  
  todayMenuStore.addRecipe(currentRecipe.value);
  loadSingleRecipe(); // Load the next recipe after adding
}

// Alias reRoll to handleNext for clarity in the template
const reRoll = handleNext;

function closeDialog() {
  dialogVisible.value = false;
}

// Watch for the dialog opening
watch(() => props.modelValue, (newValue) => {
  if (newValue) {
    loadSingleRecipe(); // Load a recipe when dialog opens
  } else {
    // Reset state when dialog closes
    currentRecipe.value = null;
    error.value = null;
  }
});

</script>

<style>
@import '@/assets/components/random-recipe-dialog.css';
</style>
