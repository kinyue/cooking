<template>
  <v-dialog v-model="dialogVisible" max-width="600px">
    <v-card>
      <v-card-title class="text-h5 pa-4">
        今日菜单
        <v-spacer></v-spacer>
        <v-btn icon @click="closeDialog">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <v-divider></v-divider>
      
      <v-card-text class="pa-4">
        <div v-if="menuItems.length === 0" class="text-center py-4 text-medium-emphasis">
          暂未添加任何菜谱
        </div>
        <div v-else>
          <!-- Recipes Section -->
          <div class="recipes-section mb-4">
            <div class="text-subtitle-1 font-weight-medium mb-2">
              <v-icon icon="mdi-book-open-variant" class="mr-1"></v-icon>
              已选菜谱
            </div>
            <v-list>
              <v-list-item
                v-for="recipe in menuItems"
                :key="recipe.id"
                :value="recipe"
              >
                <template v-slot:prepend>
                  <v-checkbox-btn
                    v-model="recipe.checked"
                    density="comfortable"
                  ></v-checkbox-btn>
                </template>
                <v-list-item-title>{{ recipe.name }}</v-list-item-title>
                <template v-slot:append>
                  <v-btn
                    icon="mdi-close"
                    size="small"
                    variant="text"
                    density="comfortable"
                    color="error"
                    @click="removeRecipe(recipe.id)"
                  ></v-btn>
                </template>
              </v-list-item>
            </v-list>
          </div>

          <!-- Ingredients Section -->
          <div class="ingredients-section">
            <div class="text-subtitle-1 font-weight-medium mb-2">
              <v-icon icon="mdi-food-variant" class="mr-1"></v-icon>
              所需食材
            </div>
            <v-list>
              <v-list-item
                v-for="(ingredient, index) in aggregatedIngredients"
                :key="index"
                density="comfortable"
              >
                <template v-slot:prepend>
                  <v-checkbox-btn
                    v-model="ingredient.checked"
                    density="comfortable"
                  ></v-checkbox-btn>
                </template>
                <v-list-item-title>
                  {{ ingredient.name }}
                  <span class="text-medium-emphasis">{{ ingredient.quantity }}</span>
                </v-list-item-title>
              </v-list-item>
            </v-list>
          </div>
        </div>
      </v-card-text>

      <v-divider v-if="menuItems.length > 0"></v-divider>
      
      <v-card-actions v-if="menuItems.length > 0" class="pa-4">
        <v-spacer></v-spacer>
        <v-btn
          variant="text"
          @click="clearAll"
          color="error"
          prepend-icon="mdi-delete-sweep"
        >
          清空菜单
        </v-btn>
        <v-btn
          color="primary"
          @click="clearChecked"
          :disabled="!hasCheckedItems"
          prepend-icon="mdi-check-circle"
        >
          清除已选
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { computed } from 'vue';

// Props and Emits
const props = defineProps({
  modelValue: Boolean,
  items: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['update:modelValue', 'remove', 'clear-all', 'clear-checked']);

// Local state
const dialogVisible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
});

const menuItems = computed(() => props.items);

// Computed properties
const hasCheckedItems = computed(() => {
  return menuItems.value.some(item => item.checked) ||
         aggregatedIngredients.value.some(ing => ing.checked);
});

const aggregatedIngredients = computed(() => {
  // Create a map to aggregate ingredients
  const ingredientMap = new Map();

  menuItems.value.forEach(recipe => {
    recipe.ingredients.forEach(ing => {
      const key = ing.name;
      if (!ingredientMap.has(key)) {
        ingredientMap.set(key, {
          name: ing.name,
          quantities: [],
          checked: false
        });
      }
      ingredientMap.get(key).quantities.push(ing.quantity);
    });
  });

  // Convert map to array and format quantities
  return Array.from(ingredientMap.values()).map(ing => ({
    name: ing.name,
    quantity: ing.quantities.join('、'),
    checked: ing.checked
  }));
});

// Methods
const closeDialog = () => {
  dialogVisible.value = false;
};

const removeRecipe = (recipeId) => {
  emit('remove', recipeId);
};

const clearAll = () => {
  if (confirm('确定要清空今日菜单吗？')) {
    emit('clear-all');
  }
};

const clearChecked = () => {
  emit('clear-checked');
};
</script>

<style scoped>
.recipes-section, .ingredients-section {
  border-radius: 8px;
  background-color: rgb(var(--v-theme-surface-variant));
  padding: 16px;
  margin-bottom: 16px;
}
</style>
