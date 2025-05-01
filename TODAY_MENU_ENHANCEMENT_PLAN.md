# 今日菜单功能增强开发计划 (V2 - 区分当前与历史)

## 目标
优化“今日菜单”功能，区分**当前编辑的菜单**（存储于 Pinia）和**已保存的历史菜单**（存储于后端数据库）。实现菜谱分类、当前菜单保存、历史菜单按日期查看（含版本管理）的功能。

## 核心概念区分
*   **当前编辑菜单 (Today's Working Menu):** 用户当天通过点击“添加”按钮构建的临时列表，存储在 Pinia Store 中，未持久化。
*   **历史菜单 (Historical Menu):** 用户点击“保存菜单”后，将**当前编辑菜单**的状态持久化到后端数据库的特定日期记录。

## 详细步骤

### 1. 数据库设计 (后端 - SQLite) - 无变更
*   **目标:** 存储**历史菜单**信息。
*   **Schema 文件:** `backend/data/schema_daily_menus.sql` (保持不变)。
*   **表结构:** `daily_menus` 和 `daily_menu_recipes` (保持不变)。
*   **初始化:** `init_db` 函数已更新以包含此 schema。

### 2. 后端开发 - 无变更
*   **目标:** 提供 API 用于保存和检索**历史菜单**。
*   **模型 (`backend/app/models/daily_menu.py`):** 保持不变。
*   **路由 (`backend/app/routes/daily_menus.py`):** 保持不变。API 端点用于处理历史菜单的 CRUD。
*   **注册 Blueprint:** 已完成。

### 3. 前端开发 - API 服务 - 无变更
*   **目标:** 提供调用后端历史菜单 API 的函数。
*   **文件:** `frontend/src/services/api.js` (保持不变)。函数 `fetchDailyMenu`, `fetchDatesWithMenus`, `saveDailyMenu`, `fetchMenuById` 已存在。

### 4. 前端开发 - 状态管理 (Pinia Store)
*   **目标:** 重构 Store 以管理**当前编辑菜单**和**查看的历史菜单**状态。
*   **文件:** `frontend/src/stores/todayMenu.js`
*   **状态 (State):**
    *   `todayWorkingMenuRecipes`: (ref([])) 存储当前编辑菜单的菜谱列表 `[{ recipe_id, recipe_name, meal_type, ... }]`。
    *   `viewedHistoricalMenu`: (ref(null)) 存储从后端获取的特定日期的历史菜单数据 `{ version_info: {...}, recipes: [...] }`。
    *   `viewedHistoricalDate`: (ref(null)) 当前查看的历史菜单的日期 `YYYY-MM-DD`。
    *   `availableHistoricalVersions`: (ref([])) 当前查看的历史日期的可用版本列表 `[{ id, menu_date, version, created_at }, ...]`。
    *   `selectedHistoricalVersionId`: (ref(null)) 当前查看的历史菜单的版本 ID。
    *   `datesWithHistoricalMenus`: (ref([])) 包含已保存历史菜单的日期列表 `['YYYY-MM-DD', ...]`。
    *   `isLoading`: (ref(false)) 加载状态 (可细分为加载历史日期、加载历史详情等)。
    *   `error`: (ref(null)) 错误信息。
*   **Actions:**
    *   `addRecipeToTodayWorkingMenu(recipe)`: 添加菜谱到 `todayWorkingMenuRecipes`。
    *   `removeRecipeFromTodayWorkingMenu(recipeId)`: 从 `todayWorkingMenuRecipes` 移除。
    *   `updateMealTypeInTodayWorkingMenu(recipeId, mealType)`: 更新 `todayWorkingMenuRecipes` 中菜谱的分类。
    *   `clearTodayWorkingMenu()`: 清空 `todayWorkingMenuRecipes`。
    *   `saveTodayWorkingMenu()`:
        *   获取 `todayWorkingMenuRecipes` 内容。
        *   获取**今天的日期** `YYYY-MM-DD`。
        *   调用 `saveDailyMenu(todayDate, menuData, overwrite)` API (需要实现确认覆盖逻辑)。
        *   成功后可能需要更新 `datesWithHistoricalMenus`。
    *   `loadDatesWithHistoricalMenus()`: 调用 `fetchDatesWithMenus` API，更新 `datesWithHistoricalMenus`。
    *   `loadHistoricalMenuForDate(date)`:
        *   设置 `isLoading = true`, `error = null`。
        *   设置 `viewedHistoricalDate = date`。
        *   调用 `fetchDailyMenu(date)` API。
        *   成功后，更新 `viewedHistoricalMenu` (使用 `latest_menu`), `availableHistoricalVersions`, `selectedHistoricalVersionId`。
        *   处理错误。
        *   设置 `isLoading = false`。
    *   `loadHistoricalMenuVersion(menuId)`:
        *   设置 `isLoading = true`, `error = null`。
        *   调用 `fetchMenuById(menuId)` API。
        *   成功后，更新 `viewedHistoricalMenu` 和 `selectedHistoricalVersionId`。
        *   处理错误。
        *   设置 `isLoading = false`。

### 5. 前端开发 - 组件
*   **目标:** 更新 UI 组件以反映新的数据流和功能。
*   **`RecipeCard.vue`:**
    *   确认“添加”按钮调用 `store.addRecipeToTodayWorkingMenu`。
    *   按钮的 `:disabled` 和 `:color` 状态应基于 `store.todayWorkingMenuRecipes` 中是否存在该菜谱。
*   **`TodayMenuDialog.vue` (显示当前编辑菜单):**
    *   数据源绑定到 `store.todayWorkingMenuRecipes`。
    *   **菜谱分类:** `v-select` 更新 `store.todayWorkingMenuRecipes` 中的 `meal_type` (通过 `updateMealTypeInTodayWorkingMenu` action)。
    *   **保存按钮:** 添加 "保存今日菜单" 按钮，触发 `store.saveTodayWorkingMenu()` action，并处理确认覆盖逻辑。
    *   **移除版本选择器:** 此对话框只显示当前未保存状态，不需要版本选择。
    *   **移除数据加载逻辑:** 此对话框不负责加载历史数据。
    *   更新“清空”、“移除已选”等按钮，使其操作 `store.todayWorkingMenuRecipes`。
*   **`AppHeader.vue`:**
    *   **日历按钮:** `@click` 调用 `openCalendar`。
    *   `openCalendar` 方法中调用 `store.loadDatesWithHistoricalMenus`。
    *   `handleDateSelect` 方法:
        *   获取选择的日期 `selectedDate`。
        *   **不再**调用 `loadMenuForDate` 或打开 `TodayMenuDialog`。
        *   **触发导航**到新的历史菜单视图（例如 `/history/:date`）或**打开新的历史菜单对话框**，并将 `selectedDate` 传递过去。
*   **新建: `HistoricalMenuView.vue` (或 `HistoricalMenuDialog.vue`):**
    *   **目标:** 显示指定日期的**历史菜单**。
    *   接收 `date` prop (或通过路由参数获取)。
    *   在组件挂载或显示时，调用 `store.loadHistoricalMenuForDate(date)`。
    *   **显示数据:** 绑定到 `store.viewedHistoricalMenu.recipes`。
    *   **版本选择:**
        *   如果 `store.availableHistoricalVersions.length > 1`，显示 `v-select`。
        *   `items` 绑定到格式化后的 `store.availableHistoricalVersions`。
        *   `v-model` 绑定到 `store.selectedHistoricalVersionId`。
        *   `@update:modelValue` 调用 `store.loadHistoricalMenuVersion`。
    *   **布局:** 可参考 `TodayMenuDialog.vue` 的列表布局，但通常为只读状态。
    *   **操作:** 可能包含“关闭”按钮，不包含“保存”按钮。
*   **前端路由 (`frontend/src/router/index.js`):** (如果选择新视图方案)
    *   添加新路由，例如：
        ```javascript
        {
          path: '/history/:date', // Date format YYYY-MM-DD
          name: 'historical-menu',
          component: () => import('../views/HistoricalMenuView.vue'), // Lazy load
          props: true // Pass route params as props
        }
        ```

## 注意事项 (保持不变)
*   **API 认证/授权:** 可能需要。
*   **错误处理:** 前后端都需要。
*   **性能:** 关注数据库查询和 API 响应。
*   **事务管理:** 后端保存操作。
*   **UI/UX:** 界面流畅，状态清晰。
*   **测试:** 覆盖新逻辑。
