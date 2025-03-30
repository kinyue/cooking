// frontend/src/services/api.js
// Service layer for interacting with the backend API

import axios from 'axios';

// Create an Axios instance with default configuration
const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:5000/api', // Your Flask backend API base URL
  headers: {
    'Content-Type': 'application/json',
    // Add any other default headers if needed (e.g., Authorization)
  }
});

// --- Recipe API Calls ---

/**
 * Fetches a list of recipes from the backend.
 * @param {object} params - Optional query parameters (filters, sort, pagination).
 * @returns {Promise<object>} A promise that resolves to the API response data (likely { data: [...] }).
 */
export const getRecipes = (params = {}) => {
  return apiClient.get('/recipes', { params });
};

/**
 * Fetches a single recipe by its ID.
 * @param {number|string} id - The ID of the recipe.
 * @returns {Promise<object>} A promise that resolves to the API response data (likely { data: {...} }).
 */
export const getRecipeById = (id) => {
  return apiClient.get(`/recipes/${id}`);
};

/**
 * Creates a new recipe.
 * @param {object} recipeData - The data for the new recipe.
 * @returns {Promise<object>} A promise that resolves to the API response data.
 */
export const createRecipe = (recipeData) => {
  // Ensure ingredients, instructions, tags are stringified JSON if backend expects strings
  const payload = { ...recipeData };
  if (Array.isArray(payload.ingredients)) {
    payload.ingredients = JSON.stringify(payload.ingredients);
  }
  if (Array.isArray(payload.instructions)) {
    payload.instructions = JSON.stringify(payload.instructions);
  }
   if (Array.isArray(payload.tags)) {
    payload.tags = JSON.stringify(payload.tags);
  }
  return apiClient.post('/recipes', payload);
};

/**
 * Updates an existing recipe.
 * @param {number|string} id - The ID of the recipe to update.
 * @param {object} recipeData - The updated data for the recipe.
 * @returns {Promise<object>} A promise that resolves to the API response data.
 */
export const updateRecipe = (id, recipeData) => {
   // Ensure ingredients, instructions, tags are stringified JSON if backend expects strings
  const payload = { ...recipeData };
  if (Array.isArray(payload.ingredients)) {
    payload.ingredients = JSON.stringify(payload.ingredients);
  }
  if (Array.isArray(payload.instructions)) {
    payload.instructions = JSON.stringify(payload.instructions);
  }
   if (Array.isArray(payload.tags)) {
    payload.tags = JSON.stringify(payload.tags);
  }
  return apiClient.put(`/recipes/${id}`, payload);
};

/**
 * Deletes a recipe by its ID.
 * @param {number|string} id - The ID of the recipe to delete.
 * @returns {Promise<object>} A promise that resolves to the API response data.
 */
export const deleteRecipe = (id) => {
  return apiClient.delete(`/recipes/${id}`);
};

// Optional: Add interceptors for handling errors globally or adding auth tokens
// apiClient.interceptors.response.use(
//   response => response,
//   error => {
//     // Handle errors (e.g., show a notification)
//     console.error('API Error:', error.response || error.message);
//     return Promise.reject(error);
//   }
// );

export default apiClient; // Export the configured instance if needed elsewhere
