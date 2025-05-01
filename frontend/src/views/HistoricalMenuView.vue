<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="10" lg="8">
        <v-card>
          <v-toolbar color="secondary" dark>
            <v-btn icon @click="goBack">
              <v-icon>mdi-arrow-left</v-icon>
            </v-btn>
            <v-toolbar-title>
              历史菜单 - {{ formattedDate }}
            </v-toolbar-title>
            <v-spacer></v-spacer>
            <!-- Add other actions if needed -->
          </v-toolbar>

          <!-- Loading and Error States -->
          <v-progress-linear indeterminate color="secondary" v-if="isLoading"></v-progress-linear>
          <v-alert type="error" v-if="errorMessage && !isLoading" class="ma-4">
            加载菜单失败: {{ errorMessage }}
          </v-alert>
          <v-alert type="info" v-if="!historicalMenuItems.length && !isLoading && !errorMessage" class="ma-4">
            该日期没有找到已保存的菜单记录。
          </v-alert>

          <v-card-text v-if="historicalMenuItems.length > 0 && !isLoading">
            <!-- Version Selector -->
            <v-select
              v-if="historicalMenuVersions.length > 1"
              :items="versionOptions"
              :model-value="historicalSelectedVersionId"
              @update:modelValue="handleVersionChange"
              label="选择菜单版本"
              variant="outlined"
              density="compact"
              hide-details
              class="mb-4"
            ></v-select>

            <!-- Display Version Info -->
            <div class="text-caption text-medium-emphasis mb-4" v-if="historicalVersionInfo">
              当前查看: 版本 {{ historicalVersionInfo.version }} (保存于 {{ new Date(historicalVersionInfo.created_at).toLocaleString('zh-CN') }})
            </div>

            <!-- Recipe List (Read-only) -->
            <v-list lines="two" class="recipe-list-historical">
              <v-list-item
                v-for="recipe in historicalMenuItems"
                :key="recipe.recipe_id"
                :title="recipe.recipe_name"
                :subtitle="`分类: ${recipe.meal_type || '未分类'}`"
                :to="{ name: 'recipe-detail', params: { id: recipe.recipe_id } }"
                link
              >
                <template v-slot:prepend>
                  <v-avatar rounded="0" class="mr-4">
                     <v-img :src="recipe.recipe_image_url || defaultImage" :alt="recipe.recipe_name" cover></v-img>
                  </v-avatar>
                </template>
                 <!-- Add more details if needed -->
              </v-list-item>
            </v-list>

          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
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

<style scoped>
.recipe-list-historical .v-list-item-subtitle {
  margin-top: 4px;
}
/* Add any specific styles for this view */
</style>
