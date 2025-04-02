import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:5000/api', // Assuming your backend is served on the same domain
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
    const response = await api.put(`/recipes/${recipeId}`, recipeData);
    return response.data;
  } catch (error) {
    console.error(`API Error updating recipe ${recipeId}:`, error);
    throw error; // Re-throw the error
  }
}

export { // Use named exports for better clarity
  getRecipes,
  getRecipeById,
  updateRecipe
};

// Keep default export for potential backward compatibility or other uses
export default {
  getRecipes,
  getRecipeById,
  updateRecipe
};
