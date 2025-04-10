<template>
  <v-dialog v-model="dialogVisible" max-width="600px">
    <v-card class="today-menu-dialog">
      <v-toolbar color="primary" class="text-white">
        <v-toolbar-title class="text-h6">
          <v-icon icon="mdi-silverware-variant" class="mr-2"></v-icon>
          今日菜单
        </v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn icon variant="text" color="white" @click="closeDialog">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-toolbar>

      <v-card-text class="pa-6">
        <div v-if="menuItems.length === 0" class="empty-state pa-8 text-center">
          <v-icon icon="mdi-playlist-plus" size="64" color="grey-lighten-1" class="mb-4"></v-icon>
          <div class="text-h6 text-grey-darken-1">暂未添加任何菜谱</div>
          <div class="text-body-2 text-grey mt-2">
            浏览菜谱并点击 <v-icon icon="mdi-plus-box" size="small" color="success"></v-icon> 添加到今日菜单
          </div>
        </div>

        <div v-else class="menu-content">
          <div class="stats-row d-flex align-center mb-6">
            <v-chip label variant="elevated" color="primary" class="mr-4">
              <v-icon start icon="mdi-book-open-variant"></v-icon>
              菜谱数量：{{ menuItems.length }}
            </v-chip>
            <v-chip label variant="elevated" color="success">
              <v-icon start icon="mdi-food-variant"></v-icon>
              食材数量：{{ aggregatedIngredients.length }}
            </v-chip>
          </div>

          <v-sheet class="recipes-section mb-6 rounded-lg" elevation="1">
            <div class="section-header d-flex align-center px-4 py-3">
              <div class="text-subtitle-1 font-weight-bold">
                <v-icon icon="mdi-book-open-variant" color="primary" class="mr-2"></v-icon>
                已选菜谱
              </div>
              <v-spacer></v-spacer>
              <v-btn variant="text" size="small" color="primary" prepend-icon="mdi-checkbox-marked-circle-outline"
                @click="toggleAllRecipes">
                {{ allRecipesChecked ? '取消全选' : '全选' }}
              </v-btn>
            </div>
            <v-divider></v-divider>
            <v-list class="recipe-list">
              <v-list-item v-for="recipe in menuItems" :key="recipe.id" :value="recipe" class="recipe-item" rounded="0">
                <template v-slot:prepend>
                  <v-checkbox-btn v-model="recipe.checked" color="primary" density="comfortable"></v-checkbox-btn>
                </template>

                <v-list-item-title class="recipe-name">
                  {{ recipe.name }}
                </v-list-item-title>
                <v-list-item-subtitle class="text-caption text-grey-darken-1 mt-1">
                  食材: {{ recipe.ingredients.map(ing => ing.name).join(', ') }}
                </v-list-item-subtitle>

                <template v-slot:append>
                  <div class="d-flex align-center">
                    <v-chip size="small" variant="flat" color="primary" class="mr-2">
                      {{ recipe.ingredients.length }}种食材
                    </v-chip>
                    <v-btn icon="mdi-delete" size="small" variant="text" color="error"
                      @click="removeRecipe(recipe.id)"></v-btn>
                  </div>
                </template>
              </v-list-item>
            </v-list>
          </v-sheet>

          <v-sheet class="ingredients-section rounded-lg" elevation="1">
            <div class="section-header d-flex align-center px-4 py-3">
              <div class="text-subtitle-1 font-weight-bold">
                <v-icon icon="mdi-food-variant" color="primary" class="mr-2"></v-icon>
                所需食材
              </div>
              <v-spacer></v-spacer>
              <v-btn variant="text" size="small" color="primary" prepend-icon="mdi-checkbox-marked-circle-outline"
                @click="toggleAllIngredients">
                {{ allIngredientsChecked ? '取消全选' : '全选' }}
              </v-btn>
            </div>
            <v-divider></v-divider>
            <v-list class="ingredient-list">
              <v-list-item v-for="(ingredient, index) in aggregatedIngredients" :key="index" density="comfortable"
                class="ingredient-item" rounded="0">
                <template v-slot:prepend>
                  <v-checkbox-btn :model-value="ingredient.checked"
                    @update:modelValue="handleIngredientToggle(ingredient.name, ingredient.checked)"
                    color="success" density="comfortable"></v-checkbox-btn>
                </template>
                <v-list-item-title>
                  {{ ingredient.name }}
                  <span class="text-grey ml-2">x{{ ingredient.count }}</span>
                </v-list-item-title>
              </v-list-item>
            </v-list>
          </v-sheet>
        </div>
      </v-card-text>

      <v-divider v-if="menuItems.length > 0"></v-divider>

      <v-card-actions v-if="menuItems.length > 0" class="pa-4">
        <v-btn variant="tonal" color="primary" @click="copyToClipboard" prepend-icon="mdi-content-copy" class="mr-2">
          复制清单
        </v-btn>
        <v-btn variant="tonal" color="success" @click="exportList" prepend-icon="mdi-file-export-outline">
          导出清单
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn variant="outlined" color="error" @click="confirmClearAll" prepend-icon="mdi-playlist-remove"
          class="mr-2">
          清空菜单
        </v-btn>
        <v-btn variant="elevated" color="error" @click="clearChecked" :disabled="!hasCheckedItems"
          prepend-icon="mdi-delete-sweep">
          移除已选
        </v-btn>
      </v-card-actions>
    </v-card>

    <v-dialog v-model="showConfirmDialog" width="auto">
      <v-card class="pa-4">
        <v-card-title class="text-h6 mb-2">
          <v-icon icon="mdi-alert" color="warning" class="mr-2"></v-icon>
          确认清空
        </v-card-title>
        <v-card-text>确定要清空今日菜单吗？此操作无法撤销。</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="showConfirmDialog = false">
            取消
          </v-btn>
          <v-btn color="error" @click="handleConfirmClear" variant="elevated">
            确定清空
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-dialog>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useTodayMenuStore } from '@/stores/todayMenu';

const todayMenu = useTodayMenuStore();

// Props and Emits
const props = defineProps({
  modelValue: Boolean,
  items: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['update:modelValue', 'remove', 'clear-all', 'clear-checked', 'update:snackbar']);

// Interface for snackbar message
const showSnackbar = (message, color = 'success') => {
  emit('update:snackbar', {
    show: true,
    text: message,
    color: color
  });
};

/**
 * Formats the today's menu into a Markdown string for clipboard copy and export.
 * Includes:
 * 1. Checked recipes, each followed by a flat list of its original ingredients.
 * 2. A separate list of checked ingredients from the aggregated shopping list.
 * @returns {string} The formatted Markdown string.
 */
const formatList = () => {
  let text = '# 今日菜单\n\n';
  let hasContent = false; // Flag to track if any content is added

  // --- Section 1: Checked Recipes with their original ingredients ---
  const checkedRecipes = menuItems.value.filter(recipe => recipe.checked); // Get only recipes checked in the UI
  if (checkedRecipes.length > 0) {
    hasContent = true;
    text += '## 已选菜谱\n\n';
    checkedRecipes.forEach((recipe) => {
      text += `- ${recipe.name}\n`; // Add recipe name as a list item
      // Add original ingredients as a flat, comma-separated list on the next line (indented slightly for clarity)
      if (recipe.ingredients && recipe.ingredients.length > 0) {
        const ingredientNames = recipe.ingredients.map(ing => ing.name).join(', ');
        text += `  (食材: ${ingredientNames})\n`; // Indented line showing flat ingredients list
      } else {
        text += `  (无特定食材)\n`; // Indicate if a recipe has no specific ingredients listed
      }
    });
  }

  // --- Section 2: Checked Aggregated Ingredients (Shopping List) ---
  // Filter the aggregated list for items that are actually checked in the UI's shopping list section
  const checkedShoppingListIngredients = aggregatedIngredients.value.filter(ingredient => ingredient.checked);
  if (checkedShoppingListIngredients.length > 0) {
    hasContent = true;
    text += '\n## 所需食材 (购物清单)\n\n'; // Heading for the checked shopping list items
    checkedShoppingListIngredients.forEach((ingredient) => {
      // Keep the original Markdown task list format for the shopping list
      text += `- [ ] ${ingredient.name} (x${ingredient.count})\n`; // e.g., - [ ] Tomato (x2)
    });
  }

  // Add separator and timestamp only if there was any content (checked recipes or checked ingredients)
  if (hasContent) {
    text += '\n---\n'; // Add horizontal rule separator
    text += `*导出时间：${new Date().toLocaleString('zh-CN')}*`; // Add timestamp in specified locale
  } else {
    text += '（无勾选项目）\n'; // Indicate if nothing is checked
  }


  return text;
};

// Copy to clipboard function
const copyToClipboard = async () => {
  const text = formatList();
  try {
    await navigator.clipboard.writeText(text);
    emit('update:modelValue', false); // Close dialog
    showSnackbar('菜单清单已复制到剪贴板');
  } catch (err) {
    showSnackbar('复制失败，请重试', 'error');
  }
};

// Export function
const exportList = () => {
  const text = formatList();
  const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `今日菜单_${new Date().toLocaleDateString('zh-CN')}.txt`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);

  showSnackbar('菜单清单已导出');
};

// Local state
const showConfirmDialog = ref(false);
const dialogVisible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
});

const menuItems = computed(() => props.items);

// Computed properties
const hasCheckedItems = computed(() => {
  return todayMenu.hasAnyCheckedItems; // Use the getter from the store
});

const allRecipesChecked = computed(() => {
  return menuItems.value.length > 0 && menuItems.value.every(recipe => recipe.checked);
});

const allIngredientsChecked = computed(() => {
  // Check if the aggregated list is not empty and every item in it is considered checked
  return aggregatedIngredients.value.length > 0 &&
    aggregatedIngredients.value.every(ing => ing.checked);
});

// --- Aggregated Ingredients Logic ---
// Computes the list of unique ingredients needed based on checked recipes,
// including their total count and final checked status (considering manual overrides).
const aggregatedIngredients = computed(() => {
  const ingredientCountMap = new Map();

  // Only consider ingredients from CHECKED recipes
  menuItems.value.filter(recipe => recipe.checked).forEach(recipe => {
    const uniqueIngredientsInRecipe = new Set(recipe.ingredients.map(ing => ing.name)); // Get unique ingredient names for this recipe
    uniqueIngredientsInRecipe.forEach(ingredientName => {
      ingredientCountMap.set(ingredientName, (ingredientCountMap.get(ingredientName) || 0) + 1);
    });
  });

  // Determine the final checked state based on manual overrides
  return Array.from(ingredientCountMap.entries()).map(([name, count]) => {
    let isChecked = true; // Default to checked, assuming it's needed because its recipe is checked

    // Access store state directly, Pinia handles unwrapping refs
    if (todayMenu && todayMenu.manuallyUncheckedIngredients && todayMenu.manuallyCheckedIngredients) {
      const manuallyUncheckedSet = todayMenu.manuallyUncheckedIngredients;
      const manuallyCheckedSet = todayMenu.manuallyCheckedIngredients;

      // Check if the Sets themselves are valid Set instances before calling .has()
      if (manuallyUncheckedSet instanceof Set && manuallyUncheckedSet.has(name)) {
        isChecked = false; // Manually unchecked overrides everything
      } else if (manuallyCheckedSet instanceof Set && manuallyCheckedSet.has(name)) {
        isChecked = true; // Manually checked (explicitly setting, though default is true)
      }
      // If neither manual set overrides, isChecked remains true (the default determined by recipe selection)
    }

    return {
      name: name,
      count: count,
      checked: isChecked // Final checked state for the UI checkbox
    };
  });
});

// --- Methods ---

// Handler for individual ingredient checkbox toggle in the shopping list
const handleIngredientToggle = (ingredientName, currentStatus) => {
  if (todayMenu && typeof todayMenu.toggleManualIngredientCheck === 'function') {
    todayMenu.toggleManualIngredientCheck(ingredientName, currentStatus);
  } else {
    console.error('[Dialog] todayMenu store or toggleManualIngredientCheck action not available.');
  }
};

const closeDialog = () => {
  dialogVisible.value = false;
};

const removeRecipe = (recipeId) => {
  emit('remove', recipeId);
};

const confirmClearAll = () => {
  showConfirmDialog.value = true;
};

const handleConfirmClear = () => {
  showConfirmDialog.value = false;
  emit('clear-all');
};

const clearChecked = () => {
  emit('clear-checked');
};

const toggleAllRecipes = () => {
  const newState = !allRecipesChecked.value;
  menuItems.value.forEach(recipe => {
    recipe.checked = newState;
  });
};

const toggleAllIngredients = () => {
  const shouldCheck = !allIngredientsChecked.value; // Determine the target state
  // Get all currently displayed ingredient names
  const currentIngredientNames = aggregatedIngredients.value.map(ing => ing.name);
  // Call the store action to bulk update the manual check state for these ingredients
  todayMenu.toggleAllIngredientsCheck(shouldCheck, currentIngredientNames);
};
</script>

<style>
/* Import component-specific styles */
@import '@/assets/components/today-menu-dialog.css';
</style>
