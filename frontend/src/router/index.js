// frontend/src/router/index.js
// Vue Router configuration

import { createRouter, createWebHistory } from 'vue-router'
// Import view components when they are created
import HomeView from '../views/HomeView.vue'
import RecipeDetailView from '../views/RecipeDetailView.vue'
import AddRecipeView from '../views/AddRecipeView.vue'
import EditRecipeView from '../views/EditRecipeView.vue'
// Import the new view for historical menus (lazy-loaded)
const HistoricalMenuView = () => import('../views/HistoricalMenuView.vue');
// import NotFoundView from '../views/NotFoundView.vue' // Keep commented for now

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView // Use eagerly loaded HomeView component
  },
  {
    path: '/recipes/add',
    name: 'add-recipe',
    component: AddRecipeView // Use eagerly loaded AddRecipeView
  },
  {
    // Route for viewing recipe details, uses a dynamic segment :id
    path: '/recipes/:id',
    name: 'recipe-detail',
    component: RecipeDetailView, // Use eagerly loaded RecipeDetailView
    props: true // Pass route params as props to the component
  },
  {
    // Route for editing a recipe
    path: '/recipes/:id/edit',
    name: 'edit-recipe',
    component: EditRecipeView, // Use eagerly loaded EditRecipeView
    props: true
  },
  {
    // Route for viewing historical menus for a specific date
    path: '/history/:date', // Expects date in YYYY-MM-DD format
    name: 'historical-menu',
    component: HistoricalMenuView,
    props: true // Pass route param 'date' as prop to the component
  },
  // Example of a catch-all route for 404 Not Found (optional)
  // {
  //   path: '/:pathMatch(.*)*',
  //   name: 'NotFound',
  //   component: NotFoundView // Use eagerly loaded NotFoundView if uncommented
  //   // component: () => import('../views/NotFoundView.vue')
  // }
]

const router = createRouter({
history: createWebHistory(process.env.BASE_URL || '/'), // Use HTML5 history mode
  routes // Short for `routes: routes`
})

export default router
