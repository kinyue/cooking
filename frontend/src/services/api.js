import axios from 'axios';

const api = axios.create({
  baseURL: '/api', // Assuming your backend is served on the same domain
  headers: {
    'Content-Type': 'application/json',
  },
});

const getRecipes = async () => {
  try {
    const response = await api.get('/recipes');
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    throw error; // Re-throw the error to be handled by the component
  }
};

export default {
  getRecipes,
};
