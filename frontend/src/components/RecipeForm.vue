<!-- frontend/src/components/RecipeForm.vue -->
<!-- Reusable form component for creating and editing recipes -->
<template>
  <v-form ref="form" @submit.prevent="submitForm" class="recipe-form">
    <!-- Basic Information Section -->
    <div class="form-section">
      <div class="form-section-title">
        <v-icon icon="mdi-information" color="primary" size="small"></v-icon>
        基本信息
      </div>
      <div class="form-fields-group">
        <v-text-field
          v-model="formData.name"
          label="菜谱名称"
          :rules="[rules.required]"
          required
          class="form-field mb-4"
          variant="outlined"
          density="comfortable"
        ></v-text-field>

        <v-textarea
          v-model="formData.description"
          label="描述"
          rows="3"
          class="form-field mb-4"
          variant="outlined"
          hint="简单描述一下这道菜的特点"
        ></v-textarea>

        <!-- Image Upload Section -->
        <v-file-input
          v-model="selectedImageFile"
          label="上传菜谱图片"
          accept="image/png, image/jpeg, image/gif"
          prepend-icon="mdi-camera"
          variant="outlined"
          class="form-field mb-4"
          @change="previewImage"
          :clearable="true"
          show-size
        ></v-file-input>

        <!-- Image Preview -->
        <v-img
          v-if="imagePreviewUrl"
          :src="imagePreviewUrl"
          max-height="200"
          contain
          class="mb-4 image-preview"
        ></v-img>
        <!-- Display existing image URL if editing and no new file selected -->
         <v-img
           v-else-if="isEditing && formData.image_url && !selectedImageFile"
           :src="formData.image_url"
           max-height="200"
           contain
           class="mb-4 image-preview"
         ></v-img>

      </div>
    </div>

    <!-- Ingredients Section -->
    <div class="form-section">
      <div class="form-section-title">
        <v-icon icon="mdi-food-variant" color="primary" size="small"></v-icon>
        食材配料
      </div>
      <v-textarea
        v-model="ingredientsText"
        label="食材清单"
        :rules="[rules.required]"
        required
        rows="5"
        class="form-field mb-2"
        variant="outlined"
        hint="每行一个食材，格式：名称 数量"
        persistent-hint
        placeholder="例如：&#10;豆腐 1块&#10;葱花 适量&#10;生抽 2勺"
      ></v-textarea>
    </div>

    <!-- Cooking Instructions Section -->
    <div class="form-section">
      <div class="form-section-title">
        <v-icon icon="mdi-playlist-edit" color="primary" size="small"></v-icon>
        烹饪步骤
      </div>
      <v-textarea
        v-model="instructionsText"
        label="详细步骤"
        :rules="[rules.required]"
        required
        rows="7"
        class="form-field mb-2"
        variant="outlined"
        hint="每行写一个步骤"
        persistent-hint
        placeholder="例如：&#10;1. 将豆腐切块&#10;2. 锅中放油烧热&#10;3. 放入豆腐翻炒"
      ></v-textarea>
    </div>

    <!-- Additional Details Section -->
    <div class="form-section">
      <div class="form-section-title">
        <v-icon icon="mdi-tune" color="primary" size="small"></v-icon>
        其他信息
      </div>
      
      <!-- Tags -->
      <v-combobox
        v-model="formData.tags"
        label="标签"
        multiple
        chips
        closable-chips
        clearable
        class="form-field recipe-tags mb-6"
        variant="outlined"
        hint="输入标签后按回车添加，例如：家常菜、快手菜、素食"
        persistent-hint
      ></v-combobox>

      <!-- Difficulty and Cuisine -->
      <v-row>
        <v-col cols="12" sm="6">
          <v-select
            v-model="formData.difficulty"
            :items="['简单', '中等', '困难']"
            label="难度"
            clearable
            class="form-field"
            variant="outlined"
            prepend-icon="mdi-trophy-outline"
          ></v-select>
        </v-col>
        <v-col cols="12" sm="6">
          <v-text-field
            v-model="formData.cuisine"
            label="菜系"
            clearable
            class="form-field"
            variant="outlined"
            prepend-icon="mdi-silverware-fork-knife"
            hint="例如：川菜、粤菜、西餐"
          ></v-text-field>
        </v-col>
      </v-row>

      <!-- Time and Servings -->
      <v-row>
        <v-col cols="12" sm="4">
          <v-text-field
            v-model.number="formData.prep_time_minutes"
            label="准备时间"
            type="number"
            min="0"
            clearable
            class="form-field"
            variant="outlined"
            suffix="分钟"
            prepend-icon="mdi-clock-outline"
          ></v-text-field>
        </v-col>
        <v-col cols="12" sm="4">
          <v-text-field
            v-model.number="formData.cook_time_minutes"
            label="烹饪时间"
            type="number"
            min="0"
            clearable
            class="form-field"
            variant="outlined"
            suffix="分钟"
            prepend-icon="mdi-pot-steam"
          ></v-text-field>
        </v-col>
        <v-col cols="12" sm="4">
          <v-text-field
            v-model.number="formData.servings"
            label="份量"
            type="number"
            min="1"
            clearable
            class="form-field"
            variant="outlined"
            suffix="人份"
            prepend-icon="mdi-account-group-outline"
          ></v-text-field>
        </v-col>
      </v-row>
    </div>

    <!-- Action Buttons -->
    <div class="action-buttons">
      <v-btn
        type="submit"
        color="primary"
        size="large"
        class="submit-btn"
        :loading="submitting"
        prepend-icon="mdi-check"
      >
        {{ isEditing ? '保存修改' : '创建菜谱' }}
      </v-btn>
      <v-btn
        @click="cancelForm"
        variant="outlined"
        size="large"
        class="cancel-btn"
        prepend-icon="mdi-close"
      >
        取消
      </v-btn>
    </div>
  </v-form>
</template>

<script setup>
import { ref, watch, computed, onUnmounted } from 'vue';
// Removed unused import: import { uploadRecipeImage } from '@/services/api';

// Define props and emits for TypeScript support
const props = defineProps({
  initialData: {
    type: Object,
    default: null,
  },
});

const emit = defineEmits(['submit', 'cancel']); // Add 'cancel' to emits
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
  // image_url is still needed if editing an existing recipe
});

// Image Upload State
const selectedImageFile = ref(null); // Holds the File object
const imagePreviewUrl = ref(null); // Holds the data URL for preview

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

// Image Preview Handler
const previewImage = () => {
  if (selectedImageFile.value) {
    const reader = new FileReader();
    reader.onload = (e) => {
      imagePreviewUrl.value = e.target.result;
    };
    reader.readAsDataURL(selectedImageFile.value);
  } else {
    // Clear preview if file is cleared
    imagePreviewUrl.value = null;
  }
};

// Clean up object URL on component unmount
onUnmounted(() => {
  if (imagePreviewUrl.value && imagePreviewUrl.value.startsWith('blob:')) {
    URL.revokeObjectURL(imagePreviewUrl.value);
  }
});

// Submit form handler
const submitting = ref(false); // Add submitting state

const submitForm = async () => {
  submitting.value = true; // Start loading
  const { valid } = await form.value.validate();
  if (valid) {
    try {
      // 1. Prepare recipe data (excluding image file)
      const recipeData = JSON.parse(JSON.stringify(formData.value));
      // Remove image_url if a new file is selected, backend will handle image separately
      // Keep image_url if editing and no new file is selected
      if (selectedImageFile.value) {
         delete recipeData.image_url; // Let backend handle image association
      }

      // 2. Emit submit event with recipe data (parent handles create/update)
      // The parent component will call the create/update API and get the recipe ID
      // We pass the selected image file along so the parent can upload it after creation/update
      emit('submit', { recipeData, imageFile: selectedImageFile.value });

      // Reset image state after successful submission attempt (parent confirms success)
      // selectedImageFile.value = null;
      // imagePreviewUrl.value = null;

    } catch (error) {
       console.error('Error during form submission process:', error);
       // Handle error display to user if needed
    } finally {
       submitting.value = false; // Stop loading regardless of outcome
    }
  } else {
    console.log('Form validation failed'); // Log validation failure
    submitting.value = false; // Stop loading if validation fails
  }
};

// Cancel form handler - now emits an event
const cancelForm = () => {
  emit('cancel'); // Emit cancel event instead of navigating directly
};

// Function to reset form (optional)
// Function to reset form (optional, might be called by parent)
const resetForm = () => {
  form.value?.reset(); // Reset Vuetify form state
  form.value?.resetValidation();
  formData.value = {
    name: '',
    description: '',
    image_url: '', // Keep for potential display when editing
    ingredients: [],
    instructions: [],
    tags: [],
    difficulty: null,
    cuisine: '',
    prep_time_minutes: null,
    cook_time_minutes: null,
    servings: null,
  };
  ingredientsText.value = '';
  instructionsText.value = '';
  selectedImageFile.value = null; // Reset file input
  imagePreviewUrl.value = null; // Reset preview
};

// Expose resetForm if needed by parent
defineExpose({ resetForm });

</script>

<style scoped>
@import '@/assets/components/recipe-form.css';

.image-preview {
  border: 1px solid #eee;
  border-radius: 4px;
  background-color: #f9f9f9;
}
</style>
