<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <RecipeForm formType="add" @recipe-added="onRecipeAdded" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import RecipeForm from '@/components/RecipeForm.vue';

export default {
  name: 'AddRecipeView',
  components: {
    RecipeForm,
  },
  methods: {
    onRecipeAdded(recipe) {
      // Handle recipe added event, e.g., navigate to recipe detail page
      this.$router.push({ name: 'recipe-detail', params: { id: recipe.id } });
    },
  },
};
</script>

<style scoped>
@import '@/assets/views/add-recipe-view.css';
</style>
