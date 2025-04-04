import { ref, computed } from 'vue';
import { defineStore } from 'pinia';

export const useTodayMenuStore = defineStore('todayMenu', () => {
  // State
  const items = ref([]);

  // Getters
  const count = computed(() => items.value.length);
  const allItems = computed(() => items.value);
  const hasRecipe = (recipeId) => {
    return computed(() => items.value.some(item => item.id === recipeId)).value;
  };

  // Actions
  function addRecipe(recipe) {
    // Don't add if already exists
    if (items.value.some(item => item.id === recipe.id)) {
      return false;
    }
    items.value.push({
      ...recipe,
      checked: false
    });
    return true;
  }

  function removeRecipe(recipeId) {
    const index = items.value.findIndex(item => item.id === recipeId);
    if (index !== -1) {
      items.value.splice(index, 1);
      return true;
    }
    return false;
  }

  function clearAll() {
    items.value = [];
  }

  function clearChecked() {
    items.value = items.value.filter(item => !item.checked);
  }

  return {
    // State
    items,
    // Getters
    count,
    allItems,
    // Actions
    addRecipe,
    removeRecipe,
    clearAll,
    clearChecked,
    // Expose getter
    hasRecipe
  };
});
