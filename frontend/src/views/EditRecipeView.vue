<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <RecipeForm formType="edit" :recipeId="$route.params.id" @recipeUpdated="onRecipeUpdated" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import RecipeForm from '@/components/RecipeForm.vue';

export default {
  name: 'EditRecipeView',
  components: {
    RecipeForm,
  },
  methods: {
    onRecipeUpdated(recipe) {
      // Handle recipe updated event, e.g., navigate to recipe detail page
      this.$router.push({ name: 'recipe-detail', params: { id: recipe.id } });
    },
  },
};
</script>

<style scoped>
@import '@/assets/views/edit-recipe-view.css';
</style>
