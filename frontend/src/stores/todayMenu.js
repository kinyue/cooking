import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import apiService from '@/services/api'; // Import the updated API service

// Helper to get today's date in YYYY-MM-DD format
const getTodayDateString = () => {
  const today = new Date();
  const year = today.getFullYear();
  const month = String(today.getMonth() + 1).padStart(2, '0'); // Months are 0-indexed
  const day = String(today.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
};

export const useTodayMenuStore = defineStore('todayMenu', () => {
  // --- State ---

  // State for the currently edited, unsaved menu for today
  const todayWorkingMenuRecipes = ref([]); // Stores [{ recipe_id, recipe_name, meal_type, ... }]

  // State for viewing historical menus
  const viewedHistoricalMenu = ref(null); // Stores { version_info: {...}, recipes: [...] }
  const viewedHistoricalDate = ref(null); // Stores 'YYYY-MM-DD'
  const availableHistoricalVersions = ref([]); // Stores [{ id, menu_date, version, created_at }, ...]
  const selectedHistoricalVersionId = ref(null); // Stores the ID of the viewed version

  // State for calendar highlighting
  const datesWithHistoricalMenus = ref([]); // Stores ['YYYY-MM-DD', ...]

  // General state
  const isLoading = ref(false);
  const error = ref(null);

  // --- Getters ---

  // Getters for the "Today's Working Menu"
  const currentWorkingMenuItems = computed(() => todayWorkingMenuRecipes.value);
  const currentWorkingMenuCount = computed(() => todayWorkingMenuRecipes.value.length);
  const hasRecipeInWorkingMenu = (recipeId) => {
    return computed(() => todayWorkingMenuRecipes.value.some(item => item.recipe_id === recipeId)).value;
  };

  // Getters for the "Viewed Historical Menu"
  const historicalMenuDate = computed(() => viewedHistoricalDate.value);
  const historicalMenuItems = computed(() => viewedHistoricalMenu.value?.recipes || []);
  const historicalMenuVersions = computed(() => availableHistoricalVersions.value);
  const historicalSelectedVersionId = computed(() => selectedHistoricalVersionId.value);
  const historicalVersionInfo = computed(() => viewedHistoricalMenu.value?.version_info || null);

  // Getters for Calendar
  const daysWithSavedMenu = computed(() => datesWithHistoricalMenus.value);

  // General Getters
  const loadingStatus = computed(() => isLoading.value);
  const errorMessage = computed(() => error.value);

  // --- Actions ---

  // Actions for "Today's Working Menu"
  function addRecipeToTodayWorkingMenu(recipe) {
    if (!recipe || typeof recipe.id === 'undefined') {
      console.error("Invalid recipe object passed to addRecipeToTodayWorkingMenu");
      return false;
    }
    if (todayWorkingMenuRecipes.value.some(item => item.recipe_id === recipe.id)) {
      return false; // Already exists
    }
    todayWorkingMenuRecipes.value.push({
      recipe_id: recipe.id,
      recipe_name: recipe.name,
      recipe_description: recipe.description,
      recipe_image_url: recipe.image_url,
      ingredients: recipe.ingredients, // Keep ingredients for potential display needs
      meal_type: '其他' // Default meal type
    });
    return true;
  }

  function removeRecipeFromTodayWorkingMenu(recipeId) {
    const index = todayWorkingMenuRecipes.value.findIndex(item => item.recipe_id === recipeId);
    if (index !== -1) {
      todayWorkingMenuRecipes.value.splice(index, 1);
      return true;
    }
    return false;
  }

  function updateMealTypeInTodayWorkingMenu(recipeId, mealType) {
    const recipeIndex = todayWorkingMenuRecipes.value.findIndex(item => item.recipe_id === recipeId);
    if (recipeIndex !== -1) {
      todayWorkingMenuRecipes.value[recipeIndex].meal_type = mealType;
    } else {
      console.warn(`Recipe with ID ${recipeId} not found in working menu to update meal type.`);
    }
  }

  function clearTodayWorkingMenu() {
    todayWorkingMenuRecipes.value = [];
  }

  async function saveTodayWorkingMenu(overwrite = false) {
    isLoading.value = true;
    error.value = null;
    const dateToSave = getTodayDateString(); // Always save for today's date
    const menuDataToSave = todayWorkingMenuRecipes.value.map(item => ({
      recipe_id: item.recipe_id,
      meal_type: item.meal_type || '其他'
    }));

    // Prevent saving an empty menu? Or allow it? Allowing for now.
    // if (menuDataToSave.length === 0) {
    //   error.value = "Cannot save an empty menu.";
    //   isLoading.value = false;
    //   return { success: false, message: error.value };
    // }

    try {
      const response = await apiService.saveDailyMenu(dateToSave, menuDataToSave, overwrite);
      // After successful save, update the list of dates with menus for the calendar
      await loadDatesWithHistoricalMenus();
      // Clear the working menu after successful save? Optional, depends on desired UX.
      // clearTodayWorkingMenu();
      return { success: true, message: response.message, data: response };
    } catch (err) {
      console.error(`Failed to save working menu for date ${dateToSave}:`, err);
      const backendError = err.response?.data?.message || '';
      error.value = `无法保存今日菜单。 ${backendError}`;
      // Check specifically for overwrite conflict based on backend message (example)
      if (backendError.toLowerCase().includes("overwrite")) {
         return { success: false, message: error.value, requiresOverwriteConfirmation: true };
      }
      return { success: false, message: error.value };
    } finally {
      isLoading.value = false;
    }
  }

  // Actions for "Historical Menus"
  async function loadDatesWithHistoricalMenus() {
    // Avoid reloading if already loaded? Or always refresh? Refreshing for now.
    isLoading.value = true; // Consider a more specific loading state like isLoadingDates
    error.value = null;
    try {
      const dates = await apiService.fetchDatesWithMenus();
      datesWithHistoricalMenus.value = dates;
    } catch (err) {
      console.error("Failed to load dates with historical menus:", err);
      error.value = '无法加载有历史菜单的日期列表。';
      datesWithHistoricalMenus.value = [];
    } finally {
      isLoading.value = false;
    }
  }

  async function loadHistoricalMenuForDate(date) {
    if (!date || typeof date !== 'string') {
      console.error("loadHistoricalMenuForDate requires a valid date string.");
      error.value = "无效的日期格式。";
      return;
    }
    isLoading.value = true; // Consider isLoadingHistory
    error.value = null;
    viewedHistoricalDate.value = date;
    try {
      const response = await apiService.fetchDailyMenu(date);
      availableHistoricalVersions.value = response.versions || [];
      if (response.latest_menu) {
        selectedHistoricalVersionId.value = response.latest_menu.version_info.id;
        viewedHistoricalMenu.value = response.latest_menu; // Store the whole structure
      } else {
        selectedHistoricalVersionId.value = null;
        viewedHistoricalMenu.value = null; // No menu for this date
      }
    } catch (err) {
      console.error(`Failed to load historical menu for date ${date}:`, err);
      error.value = `无法加载日期 ${date} 的历史菜单。`;
      availableHistoricalVersions.value = [];
      selectedHistoricalVersionId.value = null;
      viewedHistoricalMenu.value = null;
    } finally {
      isLoading.value = false;
    }
  }

  async function loadHistoricalMenuVersion(menuId) {
    if (!menuId) return;
    isLoading.value = true; // Consider isLoadingHistory
    error.value = null;
    try {
      const response = await apiService.fetchMenuById(menuId);
      if (response && response.recipes && response.version_info) {
        selectedHistoricalVersionId.value = menuId;
        viewedHistoricalMenu.value = response; // Store the whole structure
        // Update viewed date if needed (should match)
        if(response.version_info.menu_date) {
            viewedHistoricalDate.value = response.version_info.menu_date;
        }
      } else {
        throw new Error("Invalid response structure from fetchMenuById");
      }
    } catch (err) {
      console.error(`Failed to load historical menu version ${menuId}:`, err);
      error.value = `无法加载历史菜单版本 ${menuId}。`;
    } finally {
      isLoading.value = false;
    }
  }

  return {
    // State refs
    todayWorkingMenuRecipes,
    viewedHistoricalMenu,
    viewedHistoricalDate,
    availableHistoricalVersions,
    selectedHistoricalVersionId,
    datesWithHistoricalMenus,
    isLoading,
    error,

    // Getters
    currentWorkingMenuItems,
    currentWorkingMenuCount,
    hasRecipeInWorkingMenu, // Renamed getter
    historicalMenuDate,
    historicalMenuItems,
    historicalMenuVersions,
    historicalSelectedVersionId,
    historicalVersionInfo,
    daysWithSavedMenu,
    loadingStatus,
    errorMessage,

    // Actions
    addRecipeToTodayWorkingMenu,
    removeRecipeFromTodayWorkingMenu,
    updateMealTypeInTodayWorkingMenu,
    clearTodayWorkingMenu,
    saveTodayWorkingMenu,
    loadDatesWithHistoricalMenus,
    loadHistoricalMenuForDate,
    loadHistoricalMenuVersion,
  };
});
