<template>
  <v-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    max-width="400"
    persistent
  >
    <v-card>
      <v-card-title class="pt-7 pb-4 px-6 text-h6 font-weight-medium d-flex align-center" style="gap: 8px">
        <v-icon icon="mdi-alert-circle" color="error" size="24"></v-icon>
        <span>确认删除</span>
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text class="pt-6 pb-4 px-6 text-body-1">
        确定要删除菜谱 <strong class="text-error">"{{ recipe?.name }}"</strong> 吗？<br>
        <span class="text-grey-darken-1">该操作无法撤销。</span>
      </v-card-text>
      <v-card-actions class="pa-6 pt-0">
        <v-spacer></v-spacer>
        <v-btn
          color="grey-darken-1"
          variant="text"
          class="mr-3"
          @click="cancel"
          :disabled="loading"
          min-width="84"
        >
          取消
        </v-btn>
        <v-btn
          color="error"
          variant="elevated"
          @click="confirm"
          :loading="loading"
          min-width="84"
        >
          删除
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

// Define props - No need to assign to 'props' if not used in script block
defineProps({
  modelValue: { // For v-model binding (controls dialog visibility)
    type: Boolean,
    required: true,
  },
  recipe: { // The recipe object to display its name
    type: Object,
    default: null, // Allow null if name isn't critical initially
  },
  loading: { // To show loading state on the confirm button
    type: Boolean,
    default: false,
  },
});

// Define emits
const emit = defineEmits(['update:modelValue', 'confirm']);

// Method to handle cancellation
const cancel = () => {
  emit('update:modelValue', false); // Close the dialog
};

// Method to handle confirmation
const confirm = () => {
  emit('confirm'); // Emit confirm event for parent to handle deletion
};
</script>
