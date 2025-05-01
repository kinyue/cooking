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

      <!-- Loading State -->
      <v-progress-linear indeterminate color="primary" v-if="isLoading"></v-progress-linear>


      <!-- Show content when not loading, regardless of error -->
      <v-card-text class="pa-6" v-if="!isLoading">
        <!-- Use menuItems (currentWorkingMenuItems) from store -->
        <div v-if="menuItems.length === 0" class="empty-state pa-8 text-center">
          <v-icon icon="mdi-playlist-plus" size="64" color="grey-lighten-1" class="mb-4"></v-icon>
          <!-- Remove date display, as this always shows the current working menu -->
          <div class="text-h6 text-grey-darken-1">今日菜单为空</div>
          <div class="text-body-2 text-grey mt-2">
            浏览菜谱并点击 <v-icon icon="mdi-plus-box" size="small" color="success"></v-icon> 添加到当前菜单
          </div>
        </div>

        <div v-else class="menu-content">
          <!-- Use menuItems.length -->
          <div class="stats-row d-flex align-center mb-6">
            <v-chip label variant="elevated" color="primary" class="mr-4">
              <v-icon start icon="mdi-book-open-variant"></v-icon>
              菜谱数量：{{ menuItems.length }}
            </v-chip>
            <!-- Use aggregatedIngredients.length -->
            <v-chip label variant="elevated" color="success">
              <v-icon start icon="mdi-food-variant"></v-icon>
              食材数量：{{ aggregatedIngredients.length }}
            </v-chip>
          </div>

          <!-- REMOVE Version Selector -->

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
              <!-- Loop through menuItems from store, use recipe.recipe_id as key -->
              <v-list-item v-for="recipe in menuItems" :key="recipe.recipe_id" :value="recipe" class="recipe-item" rounded="0">
                <template v-slot:prepend>
                  <!-- Bind checkbox to localCheckedState using recipe_id -->
                  <v-checkbox-btn v-model="localCheckedState[recipe.recipe_id]" color="primary" density="comfortable"></v-checkbox-btn>
                </template>

                <!-- Wrap title and subtitle in a router-link, use recipe_id -->
                <router-link :to="{ name: 'recipe-detail', params: { id: recipe.recipe_id } }" class="recipe-link">
                  <v-list-item-title class="recipe-name">
                    <!-- Display recipe_name -->
                    {{ recipe.recipe_name }}
                  </v-list-item-title>
                  <v-list-item-subtitle class="text-caption text-grey-darken-1 mt-1">
                    <!-- Ensure ingredients data is available and valid before mapping -->
                    食材: {{ Array.isArray(recipe.ingredients) ? recipe.ingredients.map(ing => ing.name).join(', ') : 'N/A' }}
                  </v-list-item-subtitle>
                  <!-- Meal Type Selector -->
                  <v-select
                    :items="mealTypes"
                    :model-value="recipe.meal_type"
                    @update:modelValue="todayMenuStore.updateMealTypeInTodayWorkingMenu(recipe.recipe_id, $event)"
                    label="分类"
                    density="compact"
                    variant="outlined"
                    hide-details
                    class="meal-type-select mt-2"
                    style="max-width: 120px;"
                  ></v-select>
                </router-link>

                <template v-slot:append>
                  <div class="d-flex align-center">
                    <v-chip size="small" variant="flat" color="primary" class="mr-2">
                      <!-- Ensure ingredients data is available -->
                      {{ Array.isArray(recipe.ingredients) ? recipe.ingredients.length : 0 }}种食材
                    </v-chip>
                    <!-- Call removeRecipe with recipe_id -->
                    <v-btn icon="mdi-delete" size="small" variant="text" color="error"
                      @click="removeRecipe(recipe.recipe_id)"></v-btn>
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
              <!-- Ingredient list based on localCheckedState -->
              <v-list-item v-for="(ingredient, index) in aggregatedIngredients" :key="index" density="comfortable"
                class="ingredient-item" rounded="0">
                <template v-slot:prepend>
                  <!-- TODO: Re-evaluate ingredient checkbox logic -->
                  <v-checkbox-btn :model-value="ingredient.checked"
                    @update:modelValue="() => console.warn('Ingredient toggle TBD')"
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

      <!-- Apply flex-wrap and justify-space-between for responsive actions -->
      <v-card-actions v-if="menuItems.length > 0" class="pa-4 d-flex flex-wrap justify-space-between">
        <!-- Save Menu Button -->
        <v-btn
          variant="elevated"
          color="success"
          @click="handleSaveMenu(false)"
          :loading="isSaving"
          :disabled="isSaving"
          prepend-icon="mdi-content-save"
          class="mr-2 mb-2"
        >
          保存
        </v-btn>
        <v-btn variant="tonal" color="primary" @click="copyToClipboard" prepend-icon="mdi-content-copy" class="mr-2 mb-2"> <!-- Add mb-2 -->
          复制
        </v-btn>
        <v-btn variant="tonal" color="success" @click="exportList" prepend-icon="mdi-file-export-outline" class="mb-2 mb-2"> <!-- Add mb-2, remove mr-2 if spacer is removed -->
          导出
        </v-btn>
        <!-- Spacer might not be needed with justify-space-between, but keep for now or adjust alignment -->
        <v-spacer class="d-none d-sm-flex"></v-spacer> <!-- Hide spacer on xs screens -->
        <v-btn variant="outlined" color="error" @click="confirmClearAll" prepend-icon="mdi-playlist-remove"
          class="mr-2 mb-2"> <!-- Add mb-2 -->
          清空
        </v-btn>
        <!-- Disable button based on hasCheckedItems computed property -->
        <v-btn variant="elevated" color="error" @click="clearChecked" :disabled="!hasCheckedItems"
          prepend-icon="mdi-delete-sweep" class="mb-2"> <!-- Add mb-2 -->
          移除
        </v-btn>
      </v-card-actions>
      </v-card>

    <!-- Confirmation Dialog for Clearing -->
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

    <!-- Confirmation Dialog for Overwriting -->
    <v-dialog v-model="showOverwriteConfirm" width="auto">
        <v-card class="pa-4">
            <v-card-title class="text-h6 mb-2">
                <v-icon icon="mdi-alert-circle-outline" color="warning" class="mr-2"></v-icon>
                确认保存选项
            </v-card-title>
            <v-card-text>
                当前日期已存在菜单。您想覆盖现有菜单（版本1）还是保存为新的版本？
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn variant="text" @click="showOverwriteConfirm = false">取消</v-btn>
                <v-btn color="primary" variant="tonal" @click="handleSaveMenu(false)" :loading="isSaving" :disabled="isSaving">保存为新版本</v-btn>
                <v-btn color="warning" variant="elevated" @click="confirmOverwrite" :loading="isSaving" :disabled="isSaving">覆盖版本1</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>

  </v-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'; 
import { useTodayMenuStore } from '@/stores/todayMenu'; // Use the refactored store

const todayMenuStore = useTodayMenuStore(); // Rename store instance

// Meal type options for the select component
const mealTypes = ['早餐', '午餐', '晚餐', '夜宵', '小吃', '其他'];

// Props and Emits
const props = defineProps({
  modelValue: Boolean // Keep modelValue for dialog visibility
});
// Remove 'items' prop as data comes from store
// Remove old emits related to local item management ('remove', 'clear-all', 'clear-checked')
// Keep 'update:modelValue' and 'update:snackbar'
const emit = defineEmits(['update:modelValue', 'update:snackbar']);

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

// Get data directly from the store for the WORKING MENU
const menuItems = computed(() => todayMenuStore.currentWorkingMenuItems); // Use the working menu getter
// menuDate is not needed here as this dialog always shows the current working menu
// const menuDate = computed(() => todayMenuStore.menuDate);
const isLoading = computed(() => todayMenuStore.loadingStatus); // Keep loading state (for saving/maybe future loading)
// Remove version-related computed properties
// const menuVersions = computed(() => todayMenuStore.availableVersions);
// const currentSelectedVersionId = computed(() => todayMenuStore.selectedVersionId);

// --- Local state for UI interaction (e.g., checkboxes) ---
const localCheckedState = ref({}); // { recipeId: boolean }

// Watch the working menu items to reset local checked state
watch(menuItems, (newItems) => {
  // Initialize local checked state based on the items in the working menu
  // Preserve existing checked state if item already exists, otherwise default to false
  const newState = {};
  newItems.forEach(item => {
      newState[item.recipe_id] = localCheckedState.value[item.recipe_id] || false;
  });
  localCheckedState.value = newState;
}, { immediate: true, deep: true });


// --- Computed properties based on local state (for UI controls) ---
const allRecipesChecked = computed(() => {
  const ids = menuItems.value.map(item => item.recipe_id);
  return ids.length > 0 && ids.every(id => localCheckedState.value[id]);
});

// --- Aggregated Ingredients Logic (Based on LOCAL checked state) ---
const aggregatedIngredients = computed(() => {
  const ingredientCountMap = new Map();
  menuItems.value.filter(recipe => localCheckedState.value[recipe.recipe_id]).forEach(recipe => {
    if (Array.isArray(recipe.ingredients)) {
      const uniqueIngredientsInRecipe = new Set(recipe.ingredients.map(ing => ing.name));
      uniqueIngredientsInRecipe.forEach(ingredientName => {
        ingredientCountMap.set(ingredientName, (ingredientCountMap.get(ingredientName) || 0) + 1);
      });
    } else {
       // Use recipe_name if available for logging
       const recipeName = recipe.recipe_name || `ID ${recipe.recipe_id}`;
       console.warn(`Recipe '${recipeName}' has missing or invalid ingredients data.`);
    }
  });
  // Assume aggregated ingredients are 'checked' for shopping list UI part
  return Array.from(ingredientCountMap.entries()).map(([name, count]) => ({
    name: name,
    count: count,
    checked: true // Default for shopping list display
  }));
});

// TODO: Re-evaluate ingredient checking logic if needed for shopping list interaction.
const allIngredientsChecked = computed(() => {
    return aggregatedIngredients.value.length > 0; // Simplified: true if any ingredients listed
});

// Check if any recipe is locally checked (for enabling 'Remove Checked' button)
const hasCheckedItems = computed(() => {
    return Object.values(localCheckedState.value).some(isChecked => isChecked);
});


// --- Methods ---

// Remove watch that loads data when dialog opens - this dialog shows working state
// watch(() => props.modelValue, (newValue) => { ... });

const closeDialog = () => {
  emit('update:modelValue', false);
};

// Use store action to remove recipe LOCALLY
const removeRecipe = (recipeId) => {
  todayMenuStore. removeRecipeFromTodayWorkingMenu(recipeId);
  // Also update local checked state if the removed item was checked
  if (localCheckedState.value[recipeId]) {
      delete localCheckedState.value[recipeId];
  }
  showSnackbar('菜谱已从当前列表移除（未保存）', 'info');
};

// --- Methods for local UI state ---
const toggleAllRecipes = () => {
  const newState = !allRecipesChecked.value;
  menuItems.value.forEach(recipe => {
    localCheckedState.value[recipe.recipe_id] = newState;
  });
};

// --- Methods interacting with local state or needing adaptation ---

// TODO: Adapt formatList if copy/export is kept
// const formatList = () => { ... }
// const copyToClipboard = async () => { ... }
// const exportList = () => { ... }

// TODO: Adapt clear logic
const confirmClearAll = () => {
  // Option 1: Clear only local state
  todayMenuStore.clearTodayWorkingMenu();
  showSnackbar('当前菜单已清空（未保存）', 'info');
  // Option 2: Show confirmation then potentially call backend delete? (More complex)
};

const clearChecked = () => {
    const checkedIds = Object.entries(localCheckedState.value)
                           .filter(([, isChecked]) => isChecked)
                           .map(([id]) => parseInt(id));
    checkedIds.forEach(id => {
        todayMenuStore.removeRecipeFromTodayWorkingMenu(id);
    });
    showSnackbar('已移除选中的菜谱（未保存）', 'info');
};

// TODO: Adapt ingredient toggling if needed
// const handleIngredientToggle = (ingredientName, currentStatus) => { ... };
// const toggleAllIngredients = () => { ... };

// Remove Version Selection Logic
// function handleVersionChange(newVersionId) { ... }
// const versionOptions = computed(() => { ... });


// --- Save Menu Logic ---
const isSaving = ref(false); // Add saving state
const showOverwriteConfirm = ref(false); // State for overwrite confirmation dialog

async function handleSaveMenu(overwrite = false) {
  isSaving.value = true;
  showOverwriteConfirm.value = false; // Close confirm dialog if open
  const result = await todayMenuStore.saveTodayWorkingMenu(overwrite);
  isSaving.value = false;

  if (result.success) {
    showSnackbar('菜单已成功保存！');
    // Optionally close the dialog after saving?
    // closeDialog();
  } else {
    // Check if backend indicated a potential overwrite conflict (example logic)
    // This depends on how the backend API signals this specific case.
    // Assuming a specific error message or status code might be used.
    // For now, we'll rely on a generic error message from the store.
    // A more robust solution might involve specific error codes.
    // A simple check for now: if the error message contains 'overwrite' or similar keyword
    // This needs coordination with the backend API error response.
    if (result.message && result.message.toLowerCase().includes("overwrite")) { // Example check
        // Ask user if they want to overwrite
        showOverwriteConfirm.value = true;
        // Keep dialog open, user needs to click "Confirm Overwrite"
    } else {
        showSnackbar(`保存失败: ${result.message || '未知错误'}`, 'error');
    }
  }
}

// Function called when user confirms overwrite
function confirmOverwrite() {
    handleSaveMenu(true); // Call save again with overwrite=true
}
</script>

<style>
/* Import component-specific styles */
@import '@/assets/components/today-menu-dialog.css';

/* Style for the recipe link to remove default underline and inherit color */
.recipe-link {
  text-decoration: none;
  color: inherit;
  /* Ensure the link takes up appropriate space if needed */
  display: block; /* Or inline-block, depending on layout needs */
  flex-grow: 1; /* Allow the link to fill available space */
  margin-right: 16px; /* Add some space before the append slot */
}

.recipe-link:hover .recipe-name {
  /* Optional: Add hover effect, e.g., underline or color change */
  text-decoration: underline;
  color: rgb(var(--v-theme-primary)); /* Use Vuetify primary color on hover */
}
</style>
