<template>
  <div class="mini-recipe-card">
    <v-card flat border>
      <div class="d-flex flex-column h-100">
        <v-img
          :src="recipe.image"
          height="140"
          :alt="recipe.name"
          cover
          class="flex-grow-0"
        >
          <template v-slot:placeholder>
            <div class="d-flex align-center justify-center fill-height">
              <v-progress-circular color="grey-lighten-4" indeterminate></v-progress-circular>
            </div>
          </template>
        </v-img>
        
        <v-card-item class="pa-2 pb-1"> 
          <v-card-title class="text-subtitle-1 font-weight-bold text-truncate pa-0">
            {{ recipe.name }}
          </v-card-title>
        </v-card-item>

        <v-card-text class="pa-2 pt-0"> 
          <!-- Row 1: Time, Difficulty, Cuisine -->
          <div class="info-row mb-1"> 
            <v-chip
              size="small" 
              color="primary"
              variant="flat"
              class="px-2 font-weight-medium" 
            >
              <v-icon start size="12">mdi-clock-outline</v-icon> 
              {{ totalTime }}分钟
            </v-chip>
            <v-chip
              size="small" 
              :color="difficultyColor"
              variant="flat"
              class="px-2 font-weight-medium" 
            >
              <v-icon start size="12">mdi-fire</v-icon> 
              {{ recipe.difficulty || '未知' }}
            </v-chip>
            <v-chip
              size="small" 
              color="grey"
              variant="flat"
              class="px-2 font-weight-medium" 
            >
              <v-icon start size="12">mdi-silverware-variant</v-icon> 
              {{ cuisine }}
            </v-chip>
          </div>
          
          <!-- Row 2: Main Ingredients -->
          <div class="ingredients info-row">
            <v-icon size="small" class="text-grey me-1">mdi-food-variant</v-icon> 
            <div class="text-grey text-truncate"> 
              {{ mainIngredients }}
            </div>
          </div>
        </v-card-text>
      </div>
    </v-card>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  recipe: {
    type: Object,
    required: true,
  },
});

// Calculate total cooking time
const totalTime = computed(() => {
  const prep = props.recipe.prep_time_minutes || 0;
  const cook = props.recipe.cook_time_minutes || 0;
  return prep + cook;
});

// Extract cuisine/flavor tag (assuming it's the first tag or a specific one)
// Adjust logic if tags structure is different or more specific filtering is needed
const cuisine = computed(() => {
  if (props.recipe.tags && props.recipe.tags.length > 0) {
    // Example: Find a tag that might represent cuisine, or just take the first one
    // This might need refinement based on actual tag usage
    return props.recipe.tags[0]; 
  }
  return '未知'; // Default if no tags
});

// Get the first 3 ingredients (assuming ingredients is an array of objects with a 'name' field)
const mainIngredients = computed(() => {
  if (props.recipe.ingredients && Array.isArray(props.recipe.ingredients)) {
    return props.recipe.ingredients.slice(0, 4).map(ing => ing.name || ing).join('、'); // Join with Chinese comma
  }
  return '未知';
});

// Map difficulty to color (adjust colors as needed)
const difficultyColor = computed(() => {
  switch (props.recipe.difficulty?.toLowerCase()) {
    case '简单': return 'green';
    case '中等': return 'orange';
    case '困难': return 'red';
    default: return 'grey';
  }
});

</script>

<style>
@import '@/assets/components/mini-recipe-card.css';
</style>
