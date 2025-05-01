<template>
  <v-app-bar app color="surface" flat class="app-header">
    <router-link to="/" class="d-flex align-center text-decoration-none">
      <v-img
        src="@/assets/logo.png"
        max-height="48"
        max-width="48"
        contain
        class="ml-4 mr-3 app-logo"
        alt="App Logo"
      ></v-img>
      <div class="app-title">
        <span class="font-weight-bold text-h5 text-primary">美味秘籍</span>
      </div>
    </router-link>

    <v-spacer></v-spacer>

    <!-- Filter button for larger screens -->
    <v-btn icon @click="showFilterDrawer = true" class="header-button d-none d-sm-flex">
      <v-icon>mdi-filter-variant</v-icon>
    </v-btn>

    <!-- Use icon buttons directly on larger screens now -->
    <v-btn icon @click="isRandomRecipeDialogOpen = true" class="header-button d-none d-sm-flex">
      <v-icon>mdi-dice-5-outline</v-icon>
    </v-btn>
    <!-- Bind click event to open the add dialog -->
    <v-btn icon @click="showAddDialog = true" class="header-button d-none d-sm-flex">
      <v-icon>mdi-hamburger-plus</v-icon>
    </v-btn>
    <v-btn icon @click="showMenuDialog = true" class="header-button d-none d-sm-flex">
      <v-badge
        :content="todayMenu.currentWorkingMenuCount"
        :model-value="todayMenu.currentWorkingMenuCount > 0"
        color="error"
        floating
        overlap
      >
        <v-icon>mdi-silverware-fork-knife</v-icon>
      </v-badge>
    </v-btn>
    <!-- Calendar Button for larger screens -->
    <v-btn icon @click="openCalendar" class="header-button d-none d-sm-flex">
      <v-icon>mdi-calendar-month-outline</v-icon>
    </v-btn>

    <!-- Buttons for smaller screens -->
    <v-btn icon @click="showFilterDrawer = true" class="d-sm-none">
      <v-icon>mdi-filter-variant</v-icon>
    </v-btn>
    <v-btn icon @click="isRandomRecipeDialogOpen = true" class="d-sm-none">
      <v-icon>mdi-dice-5-outline</v-icon>
    </v-btn>
    <v-btn icon @click="showAddDialog = true" class="d-sm-none">
      <v-icon>mdi-hamburger-plus</v-icon>
    </v-btn>
    <v-btn icon @click="showMenuDialog = true" class="d-sm-none">
      <v-badge
        :content="todayMenu.currentWorkingMenuCount"
        :model-value="todayMenu.currentWorkingMenuCount > 0"
        color="error"
        floating
        overlap
      >
        <v-icon>mdi-silverware-fork-knife</v-icon>
      </v-badge>
    </v-btn>
    <v-btn icon @click="openCalendar" class="d-sm-none">
      <v-icon>mdi-calendar-month-outline</v-icon>
    </v-btn>

    <!-- Today's Menu Dialog -->
    <TodayMenuDialog
      v-model="showMenuDialog"
      @update:snackbar="snackbar = $event"
    />

    <!-- Random Recipe Dialog -->
    <RandomRecipeDialog v-model="isRandomRecipeDialogOpen" />

    <!-- Add Recipe Dialog -->
    <v-dialog v-model="showAddDialog" persistent max-width="800px">
      <v-card>
        <v-card-title>
          <span class="text-h5">添加新菜谱</span>
        </v-card-title>
        <v-card-text>
          <RecipeForm @submit="handleAddRecipeSubmit" @cancel="handleCancelAdd" />
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- Filter Drawer -->
    <FilterDrawer
      v-model="showFilterDrawer"
      @apply="handleFilterApply"
    />

    <!-- Snackbar for feedback -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="snackbar.timeout"
      location="top"
      elevation="4"
      rounded="lg"
      transition="slide-y-transition"
    >
      <template v-slot:default>
        <div class="d-flex align-center">
          <v-icon
            :icon="snackbar.color === 'success' ? 'mdi-check-circle' : 'mdi-alert-circle'"
            start
            class="mr-2"
          ></v-icon>
          <div>
            <div class="text-subtitle-2 font-weight-medium">
              {{ snackbar.color === 'success' ? '操作成功' : '操作失败' }}
            </div>
            <div class="text-body-2">{{ snackbar.text }}</div>
          </div>
        </div>
      </template>
    </v-snackbar>

    <!-- Calendar Dialog -->
    <v-dialog v-model="showCalendarDialog" width="auto">
      <v-card>
        <v-card-title>选择日期查看菜单</v-card-title>
        <v-progress-linear indeterminate color="primary" v-if="isLoadingCalendar"></v-progress-linear>
        <v-date-picker
          v-model="selectedDate"
          @update:modelValue="handleDateSelect"
          @update:month="handleMonthChange"
          color="primary"
          show-adjacent-months
          hide-header
          class="ma-2 custom-calendar-highlight"
          ref="datePickerRef" 
        ></v-date-picker> <!-- Removed :events and event-color -->
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="showCalendarDialog = false">关闭</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-app-bar>
</template>

<script setup>
// Import necessary hooks including watch, nextTick
import { ref, computed, watch, nextTick } from 'vue';
import { useTodayMenuStore } from '@/stores/todayMenu';
import TodayMenuDialog from '@/components/TodayMenuDialog.vue';
import RandomRecipeDialog from '@/components/RandomRecipeDialog.vue';
import RecipeForm from '@/components/RecipeForm.vue';
import FilterDrawer from '@/components/FilterDrawer.vue';
import { useRouter } from 'vue-router';
import { useRecipeSubmit } from '@/composables/useRecipeSubmit';

const todayMenu = useTodayMenuStore();
const showMenuDialog = ref(false);
const showAddDialog = ref(false);
const isRandomRecipeDialogOpen = ref(false);
const showFilterDrawer = ref(false);
const router = useRouter();
const datePickerRef = ref(null); // Ref for the date picker

// --- Calendar Dialog State & Logic ---
const showCalendarDialog = ref(false);
const selectedDate = ref(new Date());
const isLoadingCalendar = computed(() => todayMenu.isLoadingCalendar);

// --- Snackbar state ---
const snackbar = ref({
  show: false,
  text: '',
  color: 'success',
  timeout: 3000
});

// --- Custom Calendar Highlight Logic ---

// Function to add highlight class to calendar days
const updateCalendarHighlights = async () => {

  console.log('Updating calendar highlights...');

  await nextTick(); // Wait for DOM updates

  // Use the ref to get the date picker element, or fallback to querySelector
  const calendarElement = datePickerRef.value?.$el ?? document.querySelector('.custom-calendar-highlight');
  if (!calendarElement) {
    console.warn('Calendar element not found for highlighting.');
    return;
  }
  // More specific selector for the content area containing the day buttons
  const calendarContentElement = calendarElement.querySelector('.v-picker-outer__content') ?? calendarElement;


  // Get the dates with menus for the current view
  const datesWithMenus = todayMenu.calendarMonthMenuDates; // Use the raw 'YYYY-MM-DD' strings

  console.log('Dates with menus:', datesWithMenus);

  if (!Array.isArray(datesWithMenus)) {
      console.warn('datesWithMenus is not an array:', datesWithMenus);
      return;
  }

  // Remove existing highlights first
  calendarContentElement.querySelectorAll('.v-btn.has-menu-highlight').forEach(btn => {
    btn.classList.remove('has-menu-highlight');
  });

  // Find corresponding buttons and add the class
  datesWithMenus.forEach(dateString => {
    console.log('Processing date string for highlight:', dateString);
    try {
        const [year, month, day] = dateString.split('-').map(Number);
        // Find buttons within the calendar content area
        // Selector needs verification for Vuetify 3. Common patterns:
        // '.v-date-picker-month .v-btn'
        // '.v-date-picker-month__day > .v-btn'
        // '.v-date-picker-month__day > button' (if it's a native button)
        const dayButtons = calendarContentElement.querySelectorAll('.v-date-picker-month .v-btn'); // Adjust selector if needed

        console.log(`Found ${year}-${month}-${day} date in the calendar.`);

        dayButtons.forEach(button => {
            // Check button text content (fragile)
            if (button.textContent?.trim() === String(day)) {
                 // Add a check: Ensure the button is not for an adjacent month
                 // Vuetify might add classes like 'v-date-picker-day--adjacent' or similar
                 // Inspect the DOM to confirm the class name for adjacent days
                 const parentDayElement = button.closest('.v-date-picker-month__day'); // Find parent day container
                 if (parentDayElement && !parentDayElement.classList.contains('v-date-picker-month__day--adjacent') && !parentDayElement.classList.contains('v-date-picker-month__day--hide-adjacent')) { // Check multiple possible classes
                    button.classList.add('has-menu-highlight');
                    // console.log(`Added highlight class to button for ${dateString}`, button);
                 }
            }
        });
    } catch (e) {
        console.error(`Error processing date string ${dateString} for highlight:`, e);
    }
  });
   console.log('Finished updating calendar highlights for dates:', datesWithMenus);
};


// --- Calendar Dialog Methods ---
const openCalendar = async () => {
  try {
    showCalendarDialog.value = true;
    const initialDate = new Date();
    selectedDate.value = initialDate;
    const initialYear = initialDate.getFullYear();
    const initialMonth = initialDate.getMonth() + 1;
    await todayMenu.loadMenuDatesForMonth(initialYear, initialMonth);
    // Highlights will be updated by the watcher
  } catch (error) {
    console.error('Failed to load calendar data:', error);
    snackbar.value = { show: true, text: '加载日历数据失败', color: 'error', timeout: 3000 };
  }
};

const handleMonthChange = async (monthIndex) => { // Renamed parameter for clarity
  // The event emits the 0-based month index (e.g., 0 for January, 4 for May)
  if (typeof monthIndex !== 'number' || monthIndex < 0 || monthIndex > 11) {
      console.error("Invalid month index received from @update:month:", monthIndex);
      snackbar.value = { show: true, text: '处理月份切换失败', color: 'error', timeout: 3000 };
      return;
  }

  // Get the year from the currently selected date.
  // Note: This might be inaccurate if the user clicks a date in an adjacent month shown,
  // but it's the most straightforward way when only the month index is provided.
  const currentYear = selectedDate.value.getFullYear();
  const newMonth = monthIndex + 1; // Convert 0-based index to 1-based month

  // Update selectedDate's month for context, keeping the day and year
  // This helps keep the calendar view centered around the new month
  selectedDate.value = new Date(currentYear, monthIndex, selectedDate.value.getDate());

  console.log(`Handling month change. Year: ${currentYear}, New Month (1-based): ${newMonth}`);

  try {
    await todayMenu.loadMenuDatesForMonth(currentYear, newMonth);
    // Highlights will be updated by the watcher triggered by store change
  } catch (error) {
    console.error('Failed to load calendar data for new month:', error);
    snackbar.value = { show: true, text: '加载新月份数据失败', color: 'error', timeout: 3000 };
  }
};


const handleDateSelect = async (date) => {
  if (!(date instanceof Date)) {
      try {
          date = new Date(date);
          if (isNaN(date.getTime())) throw new Error("Invalid Date");
      } catch (e) {
          console.error("Could not convert selected value to Date:", date);
          return;
      }
  }
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const dateString = `${year}-${month}-${day}`;
  showCalendarDialog.value = false;
  router.push({ name: 'historical-menu', params: { date: dateString } });
};

// --- Use the composable for submission logic ---
const { error: submitError, submitRecipe } = useRecipeSubmit();

// --- Methods for Add Recipe Dialog ---
const handleAddRecipeSubmit = async (payload) => {
  const newRecipeId = await submitRecipe(payload);
  if (newRecipeId) {
    showAddDialog.value = false;
    snackbar.value = { show: true, text: `新菜谱添加成功！ (ID: ${newRecipeId})`, color: 'success', timeout: 3000 };
    router.push({ path: '/', query: { added: Date.now() } });
  } else {
    snackbar.value = { show: true, text: `添加菜谱失败: ${submitError.value || '请稍后再试'}`, color: 'error', timeout: 5000 };
  }
};

const handleCancelAdd = () => {
  showAddDialog.value = false;
};

// --- Methods for Filter Drawer ---
const handleFilterApply = (filters) => {
  const query = {
    ...(filters.search && { search: filters.search }),
    ...(filters.ingredientSearch && { ingredients: filters.ingredientSearch }),
    ...(filters.tags?.length > 0 && { tags: filters.tags.join(',') }),
    ...(filters.difficulty && { difficulty: filters.difficulty }),
    ...(filters.cuisine && { cuisine: filters.cuisine }),
    ...(filters.prepTimeRange && { prepTimeMin: filters.prepTimeRange[0], prepTimeMax: filters.prepTimeRange[1] }),
    ...(filters.cookTimeRange && { cookTimeMin: filters.cookTimeRange[0], cookTimeMax: filters.cookTimeRange[1] }),
    ...(filters.servings && { servingsMin: filters.servings[0], servingsMax: filters.servings[1] }),
    _t: Date.now()
  };
  Object.keys(query).forEach(key => {
    if (query[key] === undefined || query[key] === null || query[key] === '') delete query[key];
  });
  router.push({ path: '/', query });
  snackbar.value = { show: true, text: '筛选条件已应用', color: 'success', timeout: 2000 };
};


// --- Lifecycle Hooks and Watchers for Calendar Highlights ---

// Watch for changes in the dates loaded by the store
watch(() => todayMenu.calendarMonthMenuDates, (newDates, oldDates) => {
  if (JSON.stringify(newDates) !== JSON.stringify(oldDates)) {
      console.log('Detected change in calendarMonthMenuDates, updating highlights:', newDates);
      updateCalendarHighlights();
  }
}, { deep: true });

// Watch for the calendar dialog becoming visible
watch(showCalendarDialog, (isVisible) => {
  if (isVisible) {
    // Update highlights when dialog opens (data should be loaded or loading)
    updateCalendarHighlights();
  }
});

// Optional: Watch for isLoadingCalendar to ensure highlights are applied after loading finishes
watch(isLoadingCalendar, (loading) => {
    if (!loading && showCalendarDialog.value) {
        // If loading finished and dialog is open, ensure highlights are up-to-date
        updateCalendarHighlights();
    }
});

</script>

<style scoped>
@import '@/assets/components/app-header.css';



</style>
