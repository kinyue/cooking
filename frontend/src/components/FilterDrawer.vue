<template>
  <v-navigation-drawer
    v-model="drawer"
    location="right"
    temporary
    width="360"
    class="filter-drawer pa-4"
    :style="{
      top: '64px',
      height: 'calc(100vh - 64px)'
    }"
  >
    <div class="d-flex align-center justify-space-between mb-6">
      <span class="text-h6">筛选菜谱</span>
      <v-btn icon variant="text" @click="close">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </div>

    <!-- 搜索框 -->
    <v-text-field
      v-model="filters.search"
      prepend-inner-icon="mdi-magnify"
      label="搜索菜名"
      variant="outlined"
      density="comfortable"
      hide-details
      class="mb-4"
      clearable
    ></v-text-field>

    <!-- 食材搜索框 -->
    <v-text-field
      v-model="filters.ingredientSearch"
      prepend-inner-icon="mdi-carrot"
      label="搜索食材 (逗号分隔)"
      variant="outlined"
      density="comfortable"
      hide-details
      class="mb-4"
      clearable
    ></v-text-field>

    <!-- 标签多选 -->
    <v-combobox
      v-model="filters.tags"
      label="标签"
      prepend-inner-icon="mdi-tag-multiple"
      chips
      multiple
      closable-chips
      variant="outlined"
      density="comfortable"
      hide-details
      class="mb-4"
    ></v-combobox>

    <!-- 难度选择 -->
    <v-select
      v-model="filters.difficulty"
      :items="['简单', '中等', '困难']"
      label="难度"
      prepend-inner-icon="mdi-chef-hat"
      variant="outlined"
      density="comfortable"
      hide-details
      class="mb-4"
      clearable
    ></v-select>

    <!-- 菜系选择 -->
    <v-select
      v-model="filters.cuisine"
      :items="cuisineTypes"
      label="菜系"
      prepend-inner-icon="mdi-food"
      variant="outlined"
      density="comfortable"
      hide-details
      class="mb-4"
      clearable
    ></v-select>

    <!-- 准备时间范围 -->
    <div class="text-subtitle-2 mb-2">准备时间 (分钟)</div>
    <v-range-slider
      v-model="filters.prepTimeRange"
      :min="0"
      :max="120"
      :step="5"
      class="mb-4"
      hide-details
      :thumb-label="true"
    >
      <template v-slot:prepend>
        <v-text-field
          v-model="filters.prepTimeRange[0]"
          type="number"
          hide-details
          density="compact"
          variant="outlined"
          style="width: 70px"
          @change="validatePrepTimeMin"
        ></v-text-field>
      </template>
      <template v-slot:append>
        <v-text-field
          v-model="filters.prepTimeRange[1]"
          type="number"
          hide-details
          density="compact"
          variant="outlined"
          style="width: 70px"
          @change="validatePrepTimeMax"
        ></v-text-field>
      </template>
    </v-range-slider>

    <!-- 烹饪时间范围 -->
    <div class="text-subtitle-2 mb-2">烹饪时间 (分钟)</div>
    <v-range-slider
      v-model="filters.cookTimeRange"
      :min="0"
      :max="180"
      :step="5"
      class="mb-4"
      hide-details
      :thumb-label="true"
    >
      <template v-slot:prepend>
        <v-text-field
          v-model="filters.cookTimeRange[0]"
          type="number"
          hide-details
          density="compact"
          variant="outlined"
          style="width: 70px"
          @change="validateCookTimeMin"
        ></v-text-field>
      </template>
      <template v-slot:append>
        <v-text-field
          v-model="filters.cookTimeRange[1]"
          type="number"
          hide-details
          density="compact"
          variant="outlined"
          style="width: 70px"
          @change="validateCookTimeMax"
        ></v-text-field>
      </template>
    </v-range-slider>

    <!-- 份量范围 -->
    <div class="text-subtitle-2 mb-2">份量 (人份)</div>
    <v-range-slider
      v-model="filters.servings"
      :min="1"
      :max="10"
      :step="1"
      class="mb-6"
      hide-details
      :thumb-label="true"
    >
      <template v-slot:prepend>
        <v-text-field
          v-model="filters.servings[0]"
          type="number"
          hide-details
          density="compact"
          variant="outlined"
          style="width: 70px"
          @change="validateServingsMin"
        ></v-text-field>
      </template>
      <template v-slot:append>
        <v-text-field
          v-model="filters.servings[1]"
          type="number"
          hide-details
          density="compact"
          variant="outlined"
          style="width: 70px"
          @change="validateServingsMax"
        ></v-text-field>
      </template>
    </v-range-slider>

    <!-- 操作按钮 -->
    <div class="d-flex gap-4 mb-4"> <!-- Added margin-bottom -->
      <v-btn
        color="primary"
        block
        @click="applyFiltersAndClose"
        :loading="loading"
        prepend-icon="mdi-check"
      >
        应用筛选
      </v-btn>
    </div>
    <div class="d-flex gap-4">
      <v-btn
        variant="outlined"
        block
        @click="resetFiltersOnly"
        :loading="loading"
        prepend-icon="mdi-filter-remove-outline"
      >
        清除筛选
      </v-btn>
    </div>
  </v-navigation-drawer>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { useRoute } from 'vue-router';
import { debounce } from 'lodash';

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  }
});

const emit = defineEmits(['update:modelValue', 'apply']);
const route = useRoute(); // Get the current route

const drawer = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
});

const loading = ref(false);

const cuisineTypes = [
  '川菜', '粤菜', '苏菜', '浙菜', '闽菜',
  '湘菜', '鲁菜', '徽菜', '其他中国菜',
  '日本料理', '韩国料理', '意大利菜',
  '法国菜', '美式料理', '其他'
];

// 筛选条件状态
const filters = ref({
  search: '',
  ingredientSearch: '', // Add ingredient search state
  tags: [],
  difficulty: null,
  cuisine: null,
  prepTimeRange: [0, 60],
  cookTimeRange: [0, 90],
  servings: [1, 4]
});

// Function to initialize filters from route query
const initializeFiltersFromRoute = () => {
  const query = route.query;
  filters.value = {
    search: query.search || '',
    ingredientSearch: query.ingredients || '', // Initialize ingredient search
    tags: query.tags ? (Array.isArray(query.tags) ? query.tags : [query.tags]) : [], // Handle single tag string or array
    difficulty: query.difficulty || null,
    cuisine: query.cuisine || null,
    prepTimeRange: [
      query.prepTimeMin ? Number(query.prepTimeMin) : 0,
      query.prepTimeMax ? Number(query.prepTimeMax) : 60
    ],
    cookTimeRange: [
      query.cookTimeMin ? Number(query.cookTimeMin) : 0,
      query.cookTimeMax ? Number(query.cookTimeMax) : 90
    ],
    servings: [
      query.servingsMin ? Number(query.servingsMin) : 1,
      query.servingsMax ? Number(query.servingsMax) : 4
    ]
  };
};

// Watch for drawer opening to initialize filters
watch(drawer, (newValue) => {
  if (newValue) {
    initializeFiltersFromRoute();
  }
});

// Watch for route query changes to update filters (specifically tags for now)
watch(() => route.query.tags, (newTags) => {
  // Update the filter state only if the drawer is open or if the route changes
  // This prevents overwriting user input in the drawer if the route changes while it's closed.
  // However, for tag clicks, we *want* the drawer to reflect the change immediately if opened later.
  // So, we update the filter state regardless of drawer state for tags.
  filters.value.tags = newTags ? (Array.isArray(newTags) ? newTags : [newTags]) : [];
}, { deep: true }); // Use deep watch if query structure is complex, though just watching tags might be enough


// 验证函数
const validatePrepTimeMin = () => {
  const min = Number(filters.value.prepTimeRange[0]);
  const max = Number(filters.value.prepTimeRange[1]);
  filters.value.prepTimeRange[0] = Math.max(0, Math.min(min, max));
};

const validatePrepTimeMax = () => {
  const min = Number(filters.value.prepTimeRange[0]);
  const max = Number(filters.value.prepTimeRange[1]);
  filters.value.prepTimeRange[1] = Math.max(min, Math.min(max, 120));
};

const validateCookTimeMin = () => {
  const min = Number(filters.value.cookTimeRange[0]);
  const max = Number(filters.value.cookTimeRange[1]);
  filters.value.cookTimeRange[0] = Math.max(0, Math.min(min, max));
};

const validateCookTimeMax = () => {
  const min = Number(filters.value.cookTimeRange[0]);
  const max = Number(filters.value.cookTimeRange[1]);
  filters.value.cookTimeRange[1] = Math.max(min, Math.min(max, 180));
};

const validateServingsMin = () => {
  const min = Number(filters.value.servings[0]);
  const max = Number(filters.value.servings[1]);
  filters.value.servings[0] = Math.max(1, Math.min(min, max));
};

const validateServingsMax = () => {
  const min = Number(filters.value.servings[0]);
  const max = Number(filters.value.servings[1]);
  filters.value.servings[1] = Math.max(min, Math.min(max, 10));
};

// --- Filter Application Logic ---

// Debounced function for applying filters AND closing the drawer
const debouncedApplyAndCloseFilters = debounce(async () => {
  loading.value = true;
  try {
    // Emit the apply event with the current filters
    emit('apply', { ...filters.value });
  } finally {
    loading.value = false;
    drawer.value = false; // Close the drawer after applying
  }
}, 300);

// Function called by the "Apply Filters" button
const applyFiltersAndClose = () => {
  debouncedApplyAndCloseFilters();
};

// Function called by the "Clear Filters" button - Just resets the form
const resetFiltersOnly = () => {
  filters.value = {
    search: '',
    ingredientSearch: '', // Reset ingredient search
    tags: [],
    difficulty: null,
    cuisine: null,
    prepTimeRange: [0, 60],
    cookTimeRange: [0, 90],
    servings: [1, 4]
  };
  // DO NOT emit 'apply' here. Let the user click "Apply Filters" if they want.
};

const close = () => {
  drawer.value = false;
};
</script>

<style scoped>
.filter-drawer {
  overflow-y: auto;
}

.v-text-field,
.v-select,
.v-combobox {
  margin-bottom: 16px;
}
</style>
