import axios from 'axios';
import qs from 'qs'; // Import qs library

const api = axios.create({
  baseURL: 'http://127.0.0.1:5000/api', // Assuming your backend is served on the same domain
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

export {
  getRecipes,
  getRecipeById,
  fetchRandomRecipes,
  getRecipeImage,
  uploadRecipeImage, // Add upload function
  createRecipe,
  updateRecipe,
  deleteRecipe,
};

export default {
  getRecipes,
  getRecipeById,
  fetchRandomRecipes,
  getRecipeImage,
  uploadRecipeImage, // Add upload function
  createRecipe,
  updateRecipe,
  deleteRecipe
};
