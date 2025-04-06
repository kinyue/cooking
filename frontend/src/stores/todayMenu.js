import { ref, computed } from 'vue';
import { defineStore } from 'pinia';

export const useTodayMenuStore = defineStore('todayMenu', () => {
  // State
  const items = ref([]); // Stores recipe objects { id, name, ingredients, checked }
  const manuallyCheckedIngredients = ref(new Set()); // Stores names of ingredients manually checked by the user
  const manuallyUncheckedIngredients = ref(new Set()); // Stores names of ingredients manually unchecked by the user

  // Getters
  const count = computed(() => items.value.length);
  const allItems = computed(() => items.value);
  const hasRecipe = (recipeId) => {
    return computed(() => items.value.some(item => item.id === recipeId)).value;
  };
  // Getter to check if *any* item (recipe or manually tracked ingredient) is checked
  const hasAnyCheckedItems = computed(() => {
    // Check if any recipe is checked OR if any ingredient has been manually interacted with
    // (We don't directly track ingredient checked status here anymore,
    // but manual interaction implies a potential checked state change)
    return items.value.some(item => item.checked) || 
           manuallyCheckedIngredients.value.size > 0 || 
           manuallyUncheckedIngredients.value.size > 0; 
           // A simpler check might be needed depending on how clearChecked is used
  });


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

  function clearChecked() {
    // Filter out checked recipes
    items.value = items.value.filter(item => !item.checked);
    // Clear manual ingredient checks/unchecks
    manuallyCheckedIngredients.value.clear();
    manuallyUncheckedIngredients.value.clear();
  }

  // Action to handle manual checking/unchecking of ingredients
  function toggleManualIngredientCheck(ingredientName, currentAggregatedCheckedState) {
    // If the ingredient is currently considered checked (based on selected recipes and previous manual actions)
    if (currentAggregatedCheckedState) {
      // User wants to uncheck it manually
      manuallyUncheckedIngredients.value.add(ingredientName);
      manuallyCheckedIngredients.value.delete(ingredientName); // Remove if it was manually checked before
    } else {
      // User wants to check it manually
      manuallyCheckedIngredients.value.add(ingredientName);
      manuallyUncheckedIngredients.value.delete(ingredientName); // Remove if it was manually unchecked before
    }
  }

  // Action to clear all manual overrides (e.g., when clearing all recipes)
  function clearManualIngredientChecks() {
    manuallyCheckedIngredients.value.clear();
    manuallyUncheckedIngredients.value.clear();
  }
  
  // Modify clearAll to also clear manual checks
  function clearAllAndManualChecks() {
    items.value = [];
    clearManualIngredientChecks();
  }

  // Action to toggle the manual check state for a list of ingredients
  function toggleAllIngredientsCheck(shouldCheck, ingredientNames) {
    if (!ingredientNames || ingredientNames.length === 0) return;

    if (shouldCheck) {
      // User wants to check all provided ingredients
      ingredientNames.forEach(name => {
        manuallyCheckedIngredients.value.add(name);
        manuallyUncheckedIngredients.value.delete(name);
      });
    } else {
      // User wants to uncheck all provided ingredients
      ingredientNames.forEach(name => {
        manuallyUncheckedIngredients.value.add(name);
        manuallyCheckedIngredients.value.delete(name);
      });
    }
  }


  return {
    // State
    items,
    manuallyCheckedIngredients, // Expose new state
    manuallyUncheckedIngredients, // Expose new state
    // Getters
    count,
    allItems,
    hasRecipe,
    hasAnyCheckedItems, // Expose getter for overall checked status
    // Actions
    addRecipe,
    removeRecipe,
    clearAll: clearAllAndManualChecks, // Use modified clearAll
    clearChecked,
    toggleManualIngredientCheck, // Expose new action
    toggleAllIngredientsCheck, // Expose the new bulk action
    clearManualIngredientChecks // Expose new action
  };
});
