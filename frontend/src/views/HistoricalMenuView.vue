<template>
  <v-container class="py-4">
    <v-row justify="center">
      <v-col cols="12" md="10" lg="8">
        <v-card class="historical-menu-card" elevation="2">
          <v-toolbar color="primary" dark elevation="0">
            <v-btn icon @click="goBack" class="mr-2">
              <v-icon>mdi-arrow-left</v-icon>
            </v-btn>
            <v-toolbar-title class="text-h6 font-weight-medium">
              {{ formattedDate }} 的菜单记录
            </v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn icon @click="refreshData" :loading="isLoading">
              <v-icon>mdi-refresh</v-icon>
            </v-btn>
          </v-toolbar>

          <Transition name="fade" mode="out-in">
            <!-- Loading State -->
            <div v-if="isLoading" class="pa-4 text-center">
              <v-progress-circular indeterminate color="primary"></v-progress-circular>
              <div class="text-body-2 mt-2">加载中...</div>
            </div>

            <!-- Error State -->
            <v-alert
              v-else-if="errorMessage"
              type="error"
              variant="tonal"
              class="ma-4"
              closable
            >
              {{ errorMessage }}
            </v-alert>

            <!-- Empty State -->
            <div v-else-if="!historicalMenuItems.length" class="empty-state">
              <v-icon class="empty-state-icon">mdi-calendar-blank</v-icon>
              <div class="text-h6">暂无菜单记录</div>
              <div class="text-body-2 mt-2">该日期未找到已保存的菜单记录</div>
            </div>

            <!-- Content State -->
            <div v-else class="pa-4">
              <!-- Version Selector -->
              <div class="version-selector">
                <v-select
                  v-if="historicalMenuVersions.length > 1"
                  :items="versionOptions"
                  :model-value="historicalSelectedVersionId"
                  @update:modelValue="handleVersionChange"
                  label="选择菜单版本"
                  variant="outlined"
                  density="comfortable"
                  class="mb-2"
                ></v-select>

                <!-- Version Info -->
                <div class="version-info" v-if="historicalVersionInfo">
                  版本 {{ historicalVersionInfo.version }}
                  <br>
                  <span class="text-caption">
                    保存于 {{ new Date(historicalVersionInfo.created_at).toLocaleString('zh-CN') }}
                  </span>
                </div>
              </div>

              <!-- Grouped Recipe List -->
              <div v-for="(recipes, mealType) in groupedMenuItems" :key="mealType" class="menu-section mb-6">
                <div class="d-flex align-center mb-3">
                  <v-chip
                    :color="getMealTypeColor(mealType)"
                    class="meal-type-header mr-3"
                    size="large"
                  >
                    {{ mealType || '未分类' }}
                  </v-chip>
                  <div class="text-caption text-medium-emphasis">{{ recipes.length }}道菜品</div>
                </div>

                <v-list lines="three" class="recipe-list-historical">
                  <v-list-item
                    v-for="recipe in recipes"
                    :key="recipe.recipe_id"
                    :to="{ name: 'recipe-detail', params: { id: recipe.recipe_id } }"
                    class="recipe-item mb-3"
                    rounded="lg"
                  >
                    <template v-slot:prepend>
                      <v-avatar
                        size="100"
                        rounded="lg"
                        class="mr-4"
                      >
                        <v-img
                          :src="recipe.recipe_image_url || defaultImage"
                          :alt="recipe.recipe_name"
                          cover
                        ></v-img>
                      </v-avatar>
                    </template>

                    <div class="recipe-content">
                      <v-list-item-title class="text-h6 mb-2">
                        {{ recipe.recipe_name }}
                      </v-list-item-title>

                      <div class="recipe-details">
                        <div v-if="recipe.description" class="description text-body-2 mb-2">
                          {{ recipe.description }}
                        </div>
                        <div class="recipe-meta d-flex flex-wrap gap-2">
                          <v-chip
                            v-if="recipe.cooking_time"
                            size="small"
                            variant="outlined"
                            prepend-icon="mdi-clock-outline"
                          >
                            {{ recipe.cooking_time }}分钟
                          </v-chip>
                          <v-chip
                            v-if="recipe.difficulty"
                            size="small"
                            variant="outlined"
                            prepend-icon="mdi-gauge"
                          >
                            {{ recipe.difficulty }}
                          </v-chip>
                          <v-chip
                            v-if="recipe.tags && recipe.tags.length"
                            size="small"
                            variant="outlined"
                            prepend-icon="mdi-tag-outline"
                          >
                            {{ recipe.tags.join(', ') }}
                          </v-chip>
                        </div>
                      </div>
                    </div>
                  </v-list-item>
                </v-list>
              </div>
            </div>

          </Transition>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import '@/assets/views/historical-menu-view.css';
import { computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useTodayMenuStore } from '@/stores/todayMenu';

const router = useRouter();
const todayMenuStore = useTodayMenuStore();

// Props (though we get date from route param via props: true in router)
const props = defineProps({
  date: {
    type: String,
    required: true,
  },
});

// Default image placeholder
const defaultImage = 'https://via.placeholder.com/150/E0E0E0/BDBDBD?text=No+Image';

// Get state from store
const isLoading = computed(() => todayMenuStore.loadingStatus);
const errorMessage = computed(() => todayMenuStore.errorMessage);
const historicalMenuItems = computed(() => todayMenuStore.historicalMenuItems);
const historicalMenuVersions = computed(() => todayMenuStore.historicalMenuVersions);
const historicalSelectedVersionId = computed(() => todayMenuStore.historicalSelectedVersionId);
const historicalVersionInfo = computed(() => todayMenuStore.historicalVersionInfo);

// Format date for display
const formattedDate = computed(() => {
  try {
    return new Date(props.date).toLocaleDateString('zh-CN', { dateStyle: 'long' });
  } catch (e) {
    return props.date; // Fallback to raw date string if invalid
  }
});

// Group menu items by meal type
const groupedMenuItems = computed(() => {
  const groups = {};
  const mealTypeOrder = ['早餐', '午餐', '晚餐', '小食', '未分类'];
  
  // Initialize groups with preferred order
  mealTypeOrder.forEach(type => {
    groups[type] = [];
  });

  // Group items
  historicalMenuItems.value.forEach(item => {
    const type = item.meal_type || '未分类';
    if (!groups[type]) {
      groups[type] = [];
    }
    groups[type].push(item);
  });

  // Remove empty groups and maintain order
  return Object.fromEntries(
    Object.entries(groups)
      .filter(([items]) => items.length > 0)
  );
});

// Format version options for the select dropdown
const versionOptions = computed(() => {
  return historicalMenuVersions.value.map(v => ({
    title: `版本 ${v.version} (${new Date(v.created_at).toLocaleString('zh-CN', { dateStyle: 'short', timeStyle: 'short' })})`,
    value: v.id
  })).sort((a, b) => b.value - a.value); // Sort by ID descending (latest first)
});

// Method to handle version selection change
function handleVersionChange(newVersionId) {
  if (newVersionId && newVersionId !== historicalSelectedVersionId.value) {
    todayMenuStore.loadHistoricalMenuVersion(newVersionId);
  }
}

// Method to navigate back
function goBack() {
  router.go(-1); // Or router.push('/')
}

// Method to refresh data
function refreshData() {
  todayMenuStore.loadHistoricalMenuForDate(props.date);
}

// Get meal type color
function getMealTypeColor(mealType) {
  const colorMap = {
    '早餐': 'orange',
    '午餐': 'green',
    '晚餐': 'blue',
    '小食': 'purple'
  };
  return colorMap[mealType] || 'grey';
}

// Load data when component mounts or date prop changes
onMounted(() => {
  todayMenuStore.loadHistoricalMenuForDate(props.date);
});

// Watch for route param changes if user navigates between history dates directly
watch(() => props.date, (newDate) => {
  if (newDate) {
    todayMenuStore.loadHistoricalMenuForDate(newDate);
  }
});
</script>
