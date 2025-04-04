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
          <!-- Summary Stats -->
          <div class="stats-row d-flex align-center mb-6">
            <v-chip
              label
              variant="elevated"
              color="primary"
              class="mr-4"
            >
              <v-icon start icon="mdi-book-open-variant"></v-icon>
              菜谱数量：{{ menuItems.length }}
            </v-chip>
            <v-chip
              label
              variant="elevated"
              color="success"
            >
              <v-icon start icon="mdi-food-variant"></v-icon>
              食材数量：{{ aggregatedIngredients.length }}
            </v-chip>
          </div>

          <!-- Recipes Section -->
          <v-sheet
            class="recipes-section mb-6 rounded-lg"
            elevation="1"
          >
            <div class="section-header d-flex align-center px-4 py-3">
              <div class="text-subtitle-1 font-weight-bold">
                <v-icon icon="mdi-book-open-variant" color="primary" class="mr-2"></v-icon>
                已选菜谱
              </div>
              <v-spacer></v-spacer>
              <v-btn
                variant="text"
                size="small"
                color="primary"
                prepend-icon="mdi-checkbox-marked-circle-outline"
                @click="toggleAllRecipes"
              >
                {{ allRecipesChecked ? '取消全选' : '全选' }}
              </v-btn>
            </div>
            <v-divider></v-divider>
            <v-list class="recipe-list">
              <v-list-item
                v-for="recipe in menuItems"
                :key="recipe.id"
                :value="recipe"
                class="recipe-item"
                rounded="0"
              >
                <template v-slot:prepend>
                  <v-checkbox-btn
                    v-model="recipe.checked"
                    color="primary"
                    density="comfortable"
                  ></v-checkbox-btn>
                </template>

                <v-list-item-title class="recipe-name">
                  {{ recipe.name }}
                </v-list-item-title>

                <template v-slot:append>
                  <div class="d-flex align-center">
                    <v-chip
                      size="small"
                      variant="flat"
                      color="primary"
                      class="mr-2"
                    >
                      {{ recipe.ingredients.length }}种食材
                    </v-chip>
                    <v-btn
                      icon="mdi-delete"
                      size="small"
                      variant="text"
                      color="error"
                      @click="removeRecipe(recipe.id)"
                    ></v-btn>
                  </div>
                </template>
              </v-list-item>
            </v-list>
          </v-sheet>

          <!-- Ingredients Section -->
          <v-sheet
            class="ingredients-section"
            elevation="1"
            rounded="lg"
          >
            <div class="section-header d-flex align-center px-4 py-3">
              <div class="text-subtitle-1 font-weight-bold">
                <v-icon icon="mdi-food-variant" color="success" class="mr-2"></v-icon>
                所需食材
              </div>
              <v-spacer></v-spacer>
              <v-btn
                variant="text"
                size="small"
                color="success"
                prepend-icon="mdi-checkbox-marked-circle-outline"
                @click="toggleAllIngredients"
              >
                {{ allIngredientsChecked ? '取消全选' : '全选' }}
              </v-btn>
            </div>
            <v-divider></v-divider>
            <v-list class="ingredient-list">
              <v-list-item
                v-for="(ingredient, index) in aggregatedIngredients"
                :key="index"
                density="comfortable"
                class="ingredient-item"
                rounded="0"
              >
                <template v-slot:prepend>
                  <v-checkbox-btn
                    v-model="ingredient.checked"
                    color="success"
                    density="comfortable"
                  ></v-checkbox-btn>
                </template>
                <v-list-item-title>
                  {{ ingredient.name }}
                  <span class="text-grey ml-2">{{ ingredient.quantity }}</span>
                </v-list-item-title>
              </v-list-item>
            </v-list>
          </v-sheet>
        </div>
      </v-card-text>

      <v-divider v-if="menuItems.length > 0"></v-divider>
      
      <v-card-actions v-if="menuItems.length > 0" class="pa-4">
        <v-btn
          variant="tonal"
          color="primary"
          @click="copyToClipboard"
          prepend-icon="mdi-content-copy"
          class="mr-2"
        >
          复制清单
        </v-btn>
        <v-btn
          variant="tonal"
          color="success"
          @click="exportList"
          prepend-icon="mdi-file-export-outline"
        >
          导出清单
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn
          variant="outlined"
          color="error"
          @click="confirmClearAll"
          prepend-icon="mdi-bookmark-remove-multiple"
          class="mr-2"
        >
          清空菜单
        </v-btn>
        <v-btn
          variant="elevated"
          color="error"
          @click="clearChecked"
          :disabled="!hasCheckedItems"
          prepend-icon="mdi-delete-sweep"
        >
          移除已选
        </v-btn>
      </v-card-actions>
    </v-card>

    <!-- Confirmation Dialog -->
    <v-dialog v-model="showConfirmDialog" width="auto">
      <v-card class="pa-4">
        <v-card-title class="text-h6 mb-2">
          <v-icon icon="mdi-alert" color="warning" class="mr-2"></v-icon>
          确认清空
        </v-card-title>
        <v-card-text>确定要清空今日菜单吗？此操作无法撤销。</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            variant="text"
            @click="showConfirmDialog = false"
          >
            取消
          </v-btn>
          <v-btn
            color="error"
            @click="handleConfirmClear"
            variant="elevated"
          >
            确定清空
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-dialog>
</template>

<script setup>
import { ref, computed } from 'vue';

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

// Format list for clipboard and export
const formatList = () => {
  let text = '今日菜单\n\n';
  
  // Add recipes section
  text += '【已选菜谱】\n';
  menuItems.value.forEach((recipe, index) => {
    text += `${index + 1}. ${recipe.name}\n`;
  });
  
  // Add ingredients section
  text += '\n【所需食材】\n';
  aggregatedIngredients.value.forEach((ingredient, index) => {
    text += `${index + 1}. ${ingredient.name} ${ingredient.quantity}\n`;
  });
  
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
  return menuItems.value.some(item => item.checked) ||
         aggregatedIngredients.value.some(ing => ing.checked);
});

const allRecipesChecked = computed(() => {
  return menuItems.value.length > 0 && menuItems.value.every(recipe => recipe.checked);
});

const allIngredientsChecked = computed(() => {
  return aggregatedIngredients.value.length > 0 && 
         aggregatedIngredients.value.every(ing => ing.checked);
});

const aggregatedIngredients = computed(() => {
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
  const newState = !allIngredientsChecked.value;
  aggregatedIngredients.value.forEach(ingredient => {
    ingredient.checked = newState;
  });
};
</script>

<style scoped>
.today-menu-dialog {
  border-radius: 8px;
  overflow: hidden;
}

.empty-state {
  background-color: rgb(var(--v-theme-surface-variant));
  border-radius: 8px;
}

.section-header {
  background-color: rgb(var(--v-theme-surface));
}

.recipe-list, .ingredient-list {
  max-height: 300px;
  overflow-y: auto;
}

.recipe-item, .ingredient-item {
  border-radius: 0 !important;
  transition: background-color 0.2s;
}

.recipe-item:hover, .ingredient-item:hover {
  background-color: rgb(var(--v-theme-surface-variant));
}

.recipe-name {
  font-weight: 500;
}

/* Custom scrollbar styles */
.recipe-list::-webkit-scrollbar,
.ingredient-list::-webkit-scrollbar {
  width: 8px;
}

.recipe-list::-webkit-scrollbar-track,
.ingredient-list::-webkit-scrollbar-track {
  background: transparent;
}

.recipe-list::-webkit-scrollbar-thumb,
.ingredient-list::-webkit-scrollbar-thumb {
  background-color: rgba(var(--v-theme-on-surface), 0.2);
  border-radius: 4px;
}

.recipe-list::-webkit-scrollbar-thumb:hover,
.ingredient-list::-webkit-scrollbar-thumb:hover {
  background-color: rgba(var(--v-theme-on-surface), 0.3);
}

/* Fade bottom shadow for scrollable lists */
.recipe-list::after,
.ingredient-list::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 20px;
  background: linear-gradient(to top, rgb(var(--v-theme-surface)), transparent);
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.2s;
}

.recipe-list:hover::after,
.ingredient-list:hover::after {
  opacity: 1;
}
</style>
