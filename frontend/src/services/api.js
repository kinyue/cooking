import axios from 'axios';
import qs from 'qs'; // Import qs library

// Use environment variable for API base URL, fallback to localhost for development
const apiBaseUrl = process.env.VUE_APP_API_BASE_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: apiBaseUrl,
  // Configure paramsSerializer to use qs with arrayFormat: 'repeat'
  paramsSerializer: params => {
    return qs.stringify(params, { arrayFormat: 'repeat' })
  },
  headers: {
    'Content-Type': 'application/json',
  },
});

const getRecipes = async (params) => {
  try {
    const response = await api.get('/recipes', { params });
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    throw error; // Re-throw the error to be handled by the component
  }
};

// Function to get a single recipe by its ID
const getRecipeById = async (recipeId) => {
  try {
    // Construct the URL for the specific recipe
    const response = await api.get(`/recipes/${recipeId}`);
    return response.data; // Assuming backend returns the recipe object directly or within a data property
  } catch (error) {
    console.error(`API Error fetching recipe ${recipeId}:`, error);
    throw error; // Re-throw the error
  }
};

// Function to update existing recipe by its ID with new data
const updateRecipe = async (recipeId, recipeData) => {
  try {
    // Wrap recipeData inside { recipeData: ... } to match backend expectation
    const response = await api.put(`/recipes/${recipeId}`, { recipeData: recipeData });
    return response.data;
  } catch (error) {
    console.error(`API Error updating recipe ${recipeId}:`, error);
    throw error; // Re-throw the error
  }
}

// Function to delete a recipe by its ID
const deleteRecipe = async (recipeId) => {
  try {
    const response = await api.delete(`/recipes/${recipeId}`);
    return response.data;
  } catch (error) {
    console.error(`API Error deleting recipe ${recipeId}:`, error);
    throw error; // Re-throw the error
  }
}

// Function to create a new recipe (Sends JSON data)
const createRecipe = async (recipeData) => {
  try {
    // Sends JSON request to http://127.0.0.1:5000/api/recipes/
    // Backend route POST /api/recipes/ should expect JSON, potentially nested like { "recipeData": ... }
    // Adjust the payload structure if needed based on backend expectation for JSON requests.
    const response = await api.post('/recipes/', recipeData); // Sending the object directly
    return response.data;
  } catch (error) {
    console.error('API Error creating recipe:', error);
    throw error; // Re-throw the error
  }
};

// Function to fetch random recipes
const fetchRandomRecipes = async (count = 3) => {
  try {
    const response = await api.get('/recipes/random', { params: { count } });
    // Assuming the backend returns { "data": [...] }
    return response.data.data;
  } catch (error) {
    console.error('API Error fetching random recipes:', error);
    throw error; // Re-throw the error
  }
};

// Function to upload a recipe image
const uploadRecipeImage = async (recipeId, imageFile) => {
  const formData = new FormData();
  formData.append('image', imageFile); // 'image' should match the backend expected field name

  try {
    // Note: We don't set Content-Type header here,
    // axios will automatically set it to multipart/form-data with the correct boundary
    const response = await api.post(`/recipes/${recipeId}/image`, formData, {
      headers: {
        // Remove the default 'Content-Type': 'application/json' for this request
        'Content-Type': undefined,
      }
    });
    return response.data; // Assuming backend returns info about the uploaded image
  } catch (error) {
    console.error(`API Error uploading image for recipe ${recipeId}:`, error);
    throw error;
  }
};


// Function to fetch recipe image
const getRecipeImage = async (recipeId) => {
  try {
    const response = await api.get(`/recipes/${recipeId}/image`, { responseType: 'blob' });
    return URL.createObjectURL(response.data);
  } catch (error) {
    console.error(`API Error fetching image for recipe ${recipeId}:`, error);
    throw error; // Re-throw the error
  }
};

// --- Daily Menu API Calls ---

/**
 * Fetches the latest menu and available versions for a specific date.
 * @param {string} date - The date in 'YYYY-MM-DD' format.
 * @returns {Promise<object>} - Promise resolving to { latest_menu: object|null, versions: array }
 */
const fetchDailyMenu = async (date) => {
  try {
    const response = await api.get('/daily-menus', { params: { date } });
    return response.data;
  } catch (error) {
    console.error(`API Error fetching daily menu for date ${date}:`, error);
    throw error;
  }
};

/**
 * Fetches a list of all dates that have saved menus.
 * @returns {Promise<string[]>} - Promise resolving to an array of date strings ['YYYY-MM-DD', ...]
 */
const fetchDatesWithMenus = async () => {
  try {
    const response = await api.get('/daily-menus/dates');
    return response.data.dates; // Assuming backend returns { "dates": [...] }
  } catch (error) {
    console.error('API Error fetching dates with menus:', error);
    throw error;
  }
};

/**
 * Saves a new menu version for a specific date.
 * @param {string} date - The date in 'YYYY-MM-DD' format.
 * @param {Array<object>} menuData - Array of recipes, e.g., [{ recipe_id: 1, meal_type: 'Lunch' }, ...]
 * @param {boolean} overwrite - Whether to overwrite version 1 if it exists.
 * @returns {Promise<object>} - Promise resolving to the backend response (e.g., { message: string, new_menu_id: int, saved_menu: object })
 */
const saveDailyMenu = async (date, menuData, overwrite = false) => {
  try {
    // Ensure menuData is always an array, even if empty
    const recipesPayload = Array.isArray(menuData) ? menuData : [];
    const response = await api.post('/daily-menus',
      { recipes: recipesPayload }, // Request body
      { params: { date, overwrite } } // Query parameters
    );
    return response.data;
  } catch (error) {
    console.error(`API Error saving daily menu for date ${date}:`, error);
    throw error;
  }
};

/**
 * Fetches the details of a specific menu version by its ID. (Optional)
 * @param {number} menuId - The ID of the daily_menu record.
 * @returns {Promise<object>} - Promise resolving to { version_info: object, recipes: array }
 */
const fetchMenuById = async (menuId) => {
  try {
    const response = await api.get(`/daily-menus/${menuId}`);
    return response.data;
  } catch (error) {
    console.error(`API Error fetching menu version ID ${menuId}:`, error);
    throw error;
  }
};

// --- End Daily Menu API Calls ---

/**
 * Fetches a list of dates within a specific year and month that have saved menus.
 * @param {number} year - The year.
 * @param {number} month - The month (1-12).
 * @returns {Promise<string[]>} - Promise resolving to an array of date strings ['YYYY-MM-DD', ...]
 */
const fetchDatesWithMenusInMonth = async (year, month) => {
  try {
    const response = await api.get('/daily-menus/dates-in-month', { params: { year, month } });
    return response.data.dates; // Assuming backend returns { "dates": [...] }
  } catch (error) {
    console.error(`API Error fetching menu dates for ${year}-${month}:`, error);
    // Re-throw the error so the calling action in the store can handle it
    throw error;
  }
};


export {
  getRecipes,
  getRecipeById,
  fetchRandomRecipes,
  getRecipeImage,
  uploadRecipeImage,
  createRecipe,
  updateRecipe,
  deleteRecipe,
  fetchDailyMenu,
  fetchDatesWithMenus,
  saveDailyMenu,
  fetchMenuById,
  fetchDatesWithMenusInMonth, // Add the new function
};

export default {
  getRecipes,
  getRecipeById,
  fetchRandomRecipes,
  getRecipeImage,
  uploadRecipeImage,
  createRecipe,
  updateRecipe,
  deleteRecipe,
  fetchDailyMenu,
  fetchDatesWithMenus,
  saveDailyMenu,
  fetchMenuById,
  fetchDatesWithMenusInMonth, // Add the new function
};
