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

// Function to create a new recipe
const createRecipe = async (recipeData) => {
  try {
    // Correct path with trailing slash: Sends request to http://127.0.0.1:5000/api/recipes/
    const response = await api.post('/recipes/', recipeData); 
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

export {
  getRecipes,
  getRecipeById,
  fetchRandomRecipes, // Add to named exports
  getRecipeImage, // Add to named exports
  createRecipe, 
  updateRecipe,
  deleteRecipe,
};

export default {
  getRecipes,
  getRecipeById,
  fetchRandomRecipes, // Add to default export
  getRecipeImage, // Add to default export
  createRecipe, 
  updateRecipe,
  deleteRecipe
};
