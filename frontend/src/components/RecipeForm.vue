<!-- frontend/src/components/RecipeForm.vue -->
<!-- Reusable form component for creating and editing recipes -->
<template>
  <v-form ref="form" @submit.prevent="submitForm">
    <v-text-field
      v-model="formData.name"
      label="菜谱名称"
      :rules="[rules.required]"
      required
      class="mb-2"
    ></v-text-field>

    <v-textarea
      v-model="formData.description"
      label="描述 (可选)"
      rows="3"
      class="mb-2"
    ></v-textarea>

    <v-text-field
      v-model="formData.image_url"
      label="图片 URL (可选)"
      type="url"
      class="mb-2"
    ></v-text-field>

    <!-- Ingredients - Simple Textarea for now, could be improved -->
    <v-textarea
      v-model="ingredientsText"
      label="食材 (每行一个，格式：名称 数量，例如：豆腐 1块)"
      :rules="[rules.required]"
      required
      rows="5"
      class="mb-2"
      hint="例如：\n鸡蛋 2个\n面粉 100克\n糖 50克"
      persistent-hint
    ></v-textarea>

    <!-- Instructions - Simple Textarea for now, could be improved -->
    <v-textarea
      v-model="instructionsText"
      label="步骤 (每行一个)"
      :rules="[rules.required]"
      required
      rows="7"
      class="mb-2"
      hint="例如：\n1. 将鸡蛋打散。\n2. 加入面粉和糖搅拌均匀。"
      persistent-hint
    ></v-textarea>

    <!-- Tags - Using v-combobox for free-form tags -->
     <v-combobox
        v-model="formData.tags"
        label="标签 (输入后按回车添加)"
        multiple
        chips
        closable-chips
        clearable
        class="mb-2"
        hint="例如：家常菜, 简单, 快速"
        persistent-hint
      ></v-combobox>

    <v-row>
      <v-col cols="12" sm="6">
        <v-select
          v-model="formData.difficulty"
          :items="['简单', '中等', '困难']"
          label="难度 (可选)"
          clearable
          class="mb-2"
        ></v-select>
      </v-col>
      <v-col cols="12" sm="6">
         <v-text-field
            v-model="formData.cuisine"
            label="菜系 (可选)"
            clearable
            class="mb-2"
            hint="例如：川菜, 粤菜, 西餐"
          ></v-text-field>
      </v-col>
    </v-row>

     <v-row>
      <v-col cols="12" sm="4">
        <v-text-field
          v-model.number="formData.prep_time_minutes"
          label="准备时间 (分钟, 可选)"
          type="number"
          min="0"
          clearable
          class="mb-2"
        ></v-text-field>
      </v-col>
       <v-col cols="12" sm="4">
        <v-text-field
          v-model.number="formData.cook_time_minutes"
          label="烹饪时间 (分钟, 可选)"
          type="number"
          min="0"
          clearable
          class="mb-2"
        ></v-text-field>
      </v-col>
       <v-col cols="12" sm="4">
        <v-text-field
          v-model.number="formData.servings"
          label="份量 (可选)"
          type="number"
          min="1"
          clearable
          class="mb-2"
        ></v-text-field>
      </v-col>
    </v-row>

    <v-btn type="submit" color="primary" class="mr-4">
      {{ isEditing ? '更新菜谱' : '创建菜谱' }}
    </v-btn>
    <v-btn @click="cancelForm">取消</v-btn>
  </v-form>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import { useRouter } from 'vue-router';

// Define props and emits for TypeScript support
const props = defineProps({
  initialData: {
    type: Object,
    default: null,
  },
});

const emit = defineEmits(['submit']);
const router = useRouter();
const form = ref(null); // Template ref for the v-form

const isEditing = computed(() => !!props.initialData);

// Initialize form data
const formData = ref({
  name: '',
  description: '',
  image_url: '',
  ingredients: [], // Store as structured data
  instructions: [], // Store as array of strings
  tags: [],
  difficulty: null,
  cuisine: '',
  prep_time_minutes: null,
  cook_time_minutes: null,
  servings: null,
});

// Textarea models for ingredients and instructions
const ingredientsText = ref('');
const instructionsText = ref('');

// Rules for validation
const rules = {
  required: value => !!value || '此字段不能为空',
  // Add more rules as needed (e.g., number format, URL format)
};

// Populate form when initialData changes (for editing)
watch(() => props.initialData, (newData) => {
  if (newData) {
    formData.value = { ...newData }; // Copy initial data
    // Convert structured data back to text for textareas
    ingredientsText.value = (newData.ingredients || [])
        .map(ing => `${ing.name} ${ing.quantity || ''}`.trim())
        .join('\n');
    instructionsText.value = (newData.instructions || []).join('\n');
     // Ensure tags is an array
     if (typeof formData.value.tags === 'string' && formData.value.tags) {
       try {
         formData.value.tags = JSON.parse(formData.value.tags);
       } catch (e) {
         // Fallback for comma-separated string if JSON parsing fails or it's not JSON
         formData.value.tags = formData.value.tags.split(',').map(t => t.trim()).filter(t => t);
       }
     } else if (!Array.isArray(formData.value.tags)) {
        formData.value.tags = [];
     }
  } else {
    // Reset form for creation mode (optional, could be handled by parent)
    // resetForm(); // Call reset if needed when switching from edit to create
  }
}, { immediate: true }); // Run watcher immediately on mount

// Watch textareas and update structured data
watch(ingredientsText, (newText) => {
  formData.value.ingredients = newText
    .split('\n')
    .map(line => line.trim())
    .filter(line => line)
    .map(line => {
      const parts = line.split(/ (.*)/s); // Split only on the first space
      return { name: parts[0] || '', quantity: parts[1] || '' };
    });
});

watch(instructionsText, (newText) => {
  formData.value.instructions = newText
    .split('\n')
    .map(line => line.trim())
    .filter(line => line);
});


// Submit form handler
const submitForm = async () => {
  console.log('submitForm function called'); // Log function entry
  const { valid } = await form.value.validate();
  if (valid) {
    // Prepare data for submission (clone to avoid modifying original ref directly)
    const dataToSubmit = JSON.parse(JSON.stringify(formData.value));

    // Optional: Convert specific fields back to JSON strings if backend expects that
    // dataToSubmit.ingredients = JSON.stringify(dataToSubmit.ingredients);
    // dataToSubmit.instructions = JSON.stringify(dataToSubmit.instructions);
    // dataToSubmit.tags = JSON.stringify(dataToSubmit.tags);

    emit('submit', dataToSubmit);
  } else {
    console.log('Form validation failed'); // Log validation failure
  }
};

// Cancel form handler
const cancelForm = () => {
  // Navigate back or reset form based on context
  // For simplicity, just go back
  router.go(-1);
};

// Function to reset form (optional)
// const resetForm = () => {
//   form.value?.reset(); // Reset Vuetify form state
//   form.value?.resetValidation();
//   formData.value = { /* initial empty state */ };
//   ingredientsText.value = '';
//   instructionsText.value = '';
// };

</script>

<style scoped>
@import '@/assets/components/recipe-form.css';
</style>
