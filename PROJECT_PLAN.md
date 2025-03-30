# 菜谱管理 Web 应用 - 项目规划与架构设计

## 1. 项目概述与目标

**项目名称:** 美味秘籍 (示例名称)

**目标:** 开发一个用户友好、功能完善的 Web 应用程序，用于管理和浏览菜谱。用户可以查看推荐菜谱、搜索、添加、编辑和删除自己的菜谱。

**核心价值:**
*   提供一个集中管理个人菜谱的平台。
*   方便用户发现和学习新菜谱。
*   界面美观、操作直观。
*   方便用户选择当日菜谱并列出需要购买的食材。

**关键特性:**
*   菜谱列表展示（卡片式布局）。
*   菜谱详情查看。
*   菜谱的创建、编辑、删除 (CRUD)。
*   基于标签（如难度、菜系、口味等）的筛选功能。
*   响应式设计，适配不同屏幕尺寸。
*   强调代码的可维护性、可测试性和可扩展性。

## 2. 功能需求

基于提供的 ![UI 截图](frontend\design\homepage.png)和项目要求，核心功能需求如下：

*   **菜谱浏览:**
    *   以卡片形式网格布局展示菜谱列表。
    *   每张卡片显示菜谱图片（或占位符）、名称、主要食材、标签（难度、菜系、口味等）。
    *   提供“查看详情”链接/按钮。
    *   提供编辑和删除按钮。
    *   提供添加到当日菜单的按钮。
*   **菜谱详情:**
    *   显示菜谱的完整信息：名称、图片、描述、详细食材列表、烹饪步骤、标签、烹饪难度、烹饪时间等。
*   **菜谱管理 (CRUD):**
    *   **创建:** 提供表单用于添加新菜谱，包括所有必要字段。
    *   **编辑:** 提供表单用于修改现有菜谱信息。
    *   **删除:** 提供确认机制删除菜谱。
*   **筛选与推荐:**
    *   提供筛选器（可能基于标签、名称等）过滤与搜索菜谱列表。
    *   提供“推荐菜谱”功能，可能基于某种算法或随机选择，用户可选择推荐菜谱的数目。
    *   提供“今日菜单”功能，允许弹窗展示用户选择的菜谱组合以及所需的食材。
*   **用户界面:**
    *   顶部导航栏：包含 Logo、应用名称、筛选、今日菜单、用户头像/菜单。
    *   主内容区域：展示菜谱列表或详情。
    *   使用 Vuetify 组件库构建美观一致的 UI。
    *   响应式布局，适应桌面、平板和移动设备。
    *   编辑/删除以及添加到当日菜单使用icon按钮。
*   **（未来扩展）用户认证:** 虽然当前未明确要求，但架构应考虑未来加入用户注册、登录功能，实现用户私有菜谱。

## 3. 技术栈选型与理由

*   **前端:** **Vue 3 + Vuetify 3**
    *   **Vue 3:**
        *   **Composition API:** 提供更灵活、可组合的代码组织方式，易于逻辑复用和维护，特别适合复杂组件。
        *   **性能:** 相较于 Vue 2 有显著性能提升。
        *   **生态系统:** 活跃的社区和丰富的生态。
    *   **Vuetify 3:**
        *   **Material Design:** 提供一套美观、一致且功能丰富的 Material Design UI 组件，加速开发。
        *   **Vue 3 兼容:** 专为 Vue 3 设计。
        *   **响应式支持:** 内建响应式网格系统和组件。
*   **后端:** **Python + Flask**
    *   **Python:** 语法简洁，生态丰富，学习曲线平缓。
    *   **Flask:**
        *   **轻量级 & 灵活:** 微框架，核心简单，易于上手和扩展，按需添加组件。
        *   **Pythonic:** 与 Python 语言结合紧密。
        *   **社区:** 拥有庞大且活跃的社区。
        *   **适合 API 开发:** 非常适合构建 RESTful API。
*   **数据库:** **SQLite**
    *   **简单:** 无需单独的数据库服务器，数据库就是一个文件，易于部署和管理。
    *   **轻量:** 资源占用少。
    *   **开发便捷:** Python 内建 `sqlite3` 模块支持，无需额外安装驱动。
    *   **适用场景:** 非常适合小型项目、原型开发或嵌入式应用。当未来需要更高并发或更复杂查询时，可迁移至 PostgreSQL 或 MySQL。
*   **API 通信:** **RESTful API + JSON**
    *   **标准化:** 行业标准，易于理解和实现。
    *   **前后端分离:** 清晰界定前后端职责。
    *   **JSON:** 轻量级数据交换格式，JavaScript 原生支持。
*   **构建工具:** **Vue CLI**
    *   **成熟稳定:** 官方维护，经过长期验证，社区支持良好。
    *   **配置灵活:** 通过 `vue.config.js` 提供丰富的配置选项。
    *   **插件系统:** 易于集成各种常用工具和特性。
*   **开发工具:** **VS Code**
    *   **流行:** 广泛使用的代码编辑器。
    *   **扩展性:** 强大的插件生态系统（Python, Vue, Git 等）。
    *   **集成终端:** 方便执行命令。

## 4. 数据库模型 (SQLite)

核心是 `recipes` 表。

```sql
-- recipes Table Definition
CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique identifier for the recipe
    name TEXT NOT NULL,                   -- Name of the recipe (e.g., "麻婆豆腐")
    description TEXT,                     -- Optional longer description of the recipe
    ingredients TEXT NOT NULL,            -- List of ingredients, consider storing as JSON string or newline-separated text
                                          -- Example JSON: '[{"name": "Tofu", "quantity": "1 block"}, {"name": "Ground Pork", "quantity": "100g"}]'
    instructions TEXT NOT NULL,           -- Cooking steps, consider storing as JSON array of strings or newline-separated text
                                          -- Example JSON: '["Step 1: ...", "Step 2: ..."]'
    image_url TEXT,                       -- URL or path to the recipe image (optional)
    tags TEXT,                            -- Comma-separated tags (e.g., "简单,川菜,麻辣") or JSON array '["简单", "川菜", "麻辣"]'
    difficulty TEXT,                      -- Difficulty level (e.g., "简单", "中等", "困难")
    cuisine TEXT,                         -- Cuisine type (e.g., "川菜", "粤菜", "西餐")
    prep_time_minutes INTEGER,            -- Preparation time in minutes (optional)
    cook_time_minutes INTEGER,            -- Cooking time in minutes (optional)
    servings INTEGER,                     -- Number of servings (optional)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp when the recipe was created
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Timestamp when the recipe was last updated
);

-- Optional: Trigger to update updated_at timestamp on modification
CREATE TRIGGER IF NOT EXISTS update_recipes_updated_at
AFTER UPDATE ON recipes
FOR EACH ROW
BEGIN
    UPDATE recipes SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;

-- Optional: Index for faster searching/filtering by name or tags
CREATE INDEX IF NOT EXISTS idx_recipes_name ON recipes (name);
CREATE INDEX IF NOT EXISTS idx_recipes_tags ON recipes (tags); -- Effectiveness depends on how tags are queried
```

**说明:**
*   `ingredients` 和 `instructions`: 推荐使用 JSON 字符串存储结构化数据，便于前后端处理。如果需求简单，纯文本（如换行符分隔）也可以。
*   `tags`: 存储为逗号分隔的字符串或 JSON 数组。JSON 数组更易于精确查询，但 SQLite 对 JSON 的支持需要较新版本。逗号分隔字符串简单，但过滤稍麻烦（需要 `LIKE '%tag%'`）。
*   `difficulty`, `cuisine`: 可以是文本字段，前端可以提供预设选项。
*   时间戳: `created_at` 和 `updated_at` 用于追踪记录的创建和修改时间。

## 5. API 设计 (RESTful)

**Base URL:** `/api`

**数据格式:** JSON

**端点 (Endpoints):**

*   **`GET /api/recipes`**
    *   **描述:** 获取菜谱列表。
    *   **查询参数 (可选):**
        *   `search=<term>`: 按名称或描述搜索。
        *   `tags=<tag1,tag2>`: 按标签过滤 (需要后端逻辑处理逗号分隔或 JSON 数组)。
        *   `difficulty=<level>`: 按难度过滤。
        *   `cuisine=<type>`: 按菜系过滤。
        *   `sort=<field>`: 排序字段 (e.g., `name`, `created_at`).
        *   `order=<asc|desc>`: 排序方向。
        *   `page=<num>`: 页码 (用于分页)。
        *   `limit=<num>`: 每页数量 (用于分页)。
    *   **成功响应 (200 OK):**
        ```json
        {
          "data": [
            {
              "id": 1,
              "name": "麻婆豆腐",
              "image_url": "/images/mapo_tofu.jpg",
              "tags": ["简单", "川菜", "麻辣"],
              "ingredients_preview": "豆腐, 肉末, 豆瓣酱...", // 简要显示
              // ... other preview fields if needed
            },
            // ... more recipes
          ],
          "pagination": { // Optional, if pagination is implemented
            "total_items": 15,
            "total_pages": 2,
            "current_page": 1,
            "per_page": 10
          }
        }
        ```
    *   **失败响应:** `400 Bad Request` (无效参数), `500 Internal Server Error`.

*   **`POST /api/recipes`**
    *   **描述:** 创建一个新菜谱。
    *   **请求体 (Request Body):**
        ```json
        {
          "name": "红烧排骨",
          "description": "经典的家常菜...",
          "ingredients": "[{\"name\": \"排骨\", \"quantity\": \"500g\"}, ...]", // JSON string
          "instructions": "[\"Step 1: 排骨焯水\", ...]", // JSON string
          "image_url": "/images/braised_ribs.jpg",
          "tags": ["中等", "家常菜", "咸鲜"],
          "difficulty": "中等",
          "cuisine": "家常菜",
          "prep_time_minutes": 15,
          "cook_time_minutes": 60,
          "servings": 4
        }
        ```
    *   **成功响应 (201 Created):**
        ```json
        {
          "message": "Recipe created successfully",
          "data": {
            "id": 2, // ID of the newly created recipe
            "name": "红烧排骨",
            // ... other fields of the created recipe
          }
        }
        ```
    *   **失败响应:** `400 Bad Request` (无效数据或缺失字段), `500 Internal Server Error`.

*   **`GET /api/recipes/<id>`**
    *   **描述:** 获取指定 ID 的菜谱详情。
    *   **成功响应 (200 OK):**
        ```json
        {
          "data": {
            "id": 1,
            "name": "麻婆豆腐",
            "description": "...",
            "ingredients": [ // Parsed JSON
              {"name": "Tofu", "quantity": "1 block"},
              {"name": "Ground Pork", "quantity": "100g"}
            ],
            "instructions": [ // Parsed JSON
              "Step 1: ...",
              "Step 2: ..."
            ],
            "image_url": "/images/mapo_tofu.jpg",
            "tags": ["简单", "川菜", "麻辣"],
            "difficulty": "简单",
            "cuisine": "川菜",
            "prep_time_minutes": 10,
            "cook_time_minutes": 20,
            "servings": 2,
            "created_at": "2025-03-30T10:00:00Z",
            "updated_at": "2025-03-30T10:00:00Z"
          }
        }
        ```
    *   **失败响应:** `404 Not Found`, `500 Internal Server Error`.

*   **`PUT /api/recipes/<id>`**
    *   **描述:** 更新指定 ID 的菜谱。
    *   **请求体 (Request Body):** 包含需要更新的字段 (结构同 POST)。
    *   **成功响应 (200 OK):**
        ```json
        {
          "message": "Recipe updated successfully",
          "data": {
            "id": 1,
            // ... updated fields of the recipe
          }
        }
        ```
    *   **失败响应:** `400 Bad Request` (无效数据), `404 Not Found`, `500 Internal Server Error`.

*   **`DELETE /api/recipes/<id>`**
    *   **描述:** 删除指定 ID 的菜谱。
    *   **成功响应 (200 OK):**
        ```json
        {
          "message": "Recipe deleted successfully",
          "data": { "id": 1 } // ID of the deleted recipe
        }
        ```
       *(或者 204 No Content，无响应体)*
    *   **失败响应:** `404 Not Found`, `500 Internal Server Error`.

## 6. 前端架构 (Vue 3 + Vuetify 3)

**目录结构 (示例):**

```
frontend/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── assets/             # 静态资源 (图片, 字体, CSS)
│   │   └── logo.png
│   ├── components/         # 可复用 UI 组件
│   │   ├── RecipeCard.vue    # 菜谱卡片组件
│   │   ├── RecipeForm.vue    # 菜谱添加/编辑表单
│   │   ├── AppHeader.vue     # 应用头部导航
│   │   └── AppFooter.vue     # 应用底部 (如果需要)
│   ├── views/              # 页面级组件 (路由目标)
│   │   ├── HomeView.vue      # 主页 (显示菜谱列表)
│   │   ├── RecipeDetailView.vue # 菜谱详情页
│   │   ├── AddRecipeView.vue   # 添加菜谱页
│   │   └── EditRecipeView.vue  # 编辑菜谱页
│   ├── router/             # Vue Router 配置
│   │   └── index.js
│   ├── services/           # API 请求服务封装
│   │   └── api.js          # 封装 Axios/Fetch 请求
│   ├── stores/             # 状态管理 (Pinia - 可选)
│   │   ├── index.js        # Pinia 根 store
│   │   └── recipeStore.js  # 管理菜谱列表、加载状态等
│   ├── composables/        # Vue Composables (可选, 替代或补充 Pinia)
│   │   ├── useRecipes.js   # 获取和管理菜谱数据的逻辑
│   │   └── useApi.js       # 封装 API 调用状态 (loading, error)
│   ├── plugins/            # Vue 插件 (Vuetify, Axios)
│   │   ├── vuetify.js
│   │   └── axios.js        # (如果使用 Axios) 配置 Axios 实例
│   ├── App.vue             # 根组件
│   └── main.js             # 应用入口
├── .gitignore
├── package.json
├── vue.config.js         # Vue CLI 配置文件 (可选, 用于自定义构建)
└── README.md
```

**关键点:**

*   **路由 (`src/router/index.js`):** 使用 `vue-router` 定义页面路由，如 `/`, `/recipes/:id`, `/recipes/add`, `/recipes/:id/edit`。
*   **API 服务 (`src/services/api.js`):**
    *   封装对后端 API 的请求 (使用 `axios` 或 `fetch`)。
    *   创建函数如 `getRecipes()`, `getRecipeById(id)`, `createRecipe(data)`, `updateRecipe(id, data)`, `deleteRecipe(id)`。
    *   处理基础 URL、请求头、错误处理等。
*   **状态管理 (`src/stores/recipeStore.js` 或 `src/composables/useRecipes.js`):**
    *   **Pinia (推荐):** 创建一个 `recipeStore` 来管理菜谱列表、当前查看的菜谱详情、API 加载状态 (`isLoading`)、错误信息 (`error`)。提供 actions 来调用 `api.js` 中的服务并更新 state。
    *   **Composables:** 创建 `useRecipes` 可组合函数，内部管理状态 (使用 `ref`, `reactive`) 并封装调用 `api.js` 的逻辑。适合局部状态管理或简单全局状态。
*   **组件 (`src/components`, `src/views`):**
    *   `views` 负责页面布局和组合 `components`。
    *   `components` 是可复用的 UI 块。
    *   组件内通过 Pinia store 或 Composables 获取数据和调用 API actions。
    *   使用 Vuetify 组件 (`v-card`, `v-btn`, `v-text-field`, `v-select`, `v-data-table` 等) 构建界面。
*   **响应式设计:** 利用 Vuetify 的网格系统 (`v-container`, `v-row`, `v-col`) 和响应式工具类实现。

## 7. 后端架构 (Python + Flask)

**目录结构 (示例):**

```
backend/
├── app/                    # 应用核心代码
│   ├── __init__.py         # 应用工厂 (create_app function)
│   ├── routes/             # 蓝图 (Blueprints)
│   │   ├── __init__.py
│   │   └── recipes.py      # 菜谱相关的 API 路由
│   ├── models/             # 数据模型或数据访问逻辑
│   │   ├── __init__.py
│   │   └── recipe.py       # Recipe 数据模型和数据库操作函数
│   ├── services/           # (可选) 业务逻辑层
│   ├── utils/              # (可选) 工具函数
│   └── config.py           # 基础配置
├── instance/               # 实例文件夹 (不入 Git)
│   ├── config.py           # 实例特定配置 (覆盖 app/config.py)
│   └── database.db         # <<< SQLite 数据库文件 >>>
├── tests/                  # 测试代码
│   ├── __init__.py
│   └── test_recipes_api.py # 菜谱 API 测试
├── venv/                   # Python 虚拟环境 (不入 Git)
├── .env                    # (可选, 不入 Git) 环境变量
├── .flaskenv               # (可选, 不入 Git) Flask CLI 环境变量
├── .gitignore
├── requirements.txt        # Python 依赖
├── run.py / wsgi.py        # 启动脚本
└── README.md
```

**关键点:**

*   **应用工厂 (`app/__init__.py`):**
    *   定义 `create_app()` 函数。
    *   初始化 Flask app (`Flask(__name__, instance_relative_config=True)`).
    *   加载配置 (从 `app/config.py` 和 `instance/config.py`)。
    *   初始化数据库连接 (例如, 设置 `app.config['DATABASE']`)。
    *   注册蓝图 (`from .routes import recipes; app.register_blueprint(recipes.bp)`).
    *   配置 CORS (使用 `flask-cors`) 以允许前端访问。
    *   (可选) 初始化其他 Flask 扩展。
*   **蓝图 (`app/routes/recipes.py`):**
    *   创建蓝图实例 (`bp = Blueprint('recipes', __name__, url_prefix='/api/recipes')`)。
    *   定义与菜谱相关的路由 (`@bp.route('/', methods=['GET', 'POST'])`, `@bp.route('/<int:id>', methods=['GET', 'PUT', 'DELETE'])`)。
    *   在路由函数中处理请求，调用 `models/recipe.py` 中的函数与数据库交互。
    *   使用 `jsonify` 返回 JSON 响应。
    *   处理请求参数 (`request.args`, `request.get_json()`)。
*   **数据访问 (`app/models/recipe.py`):**
    *   封装所有与 `recipes` 表的数据库交互逻辑。
    *   提供函数如 `get_all_recipes(filters)`, `get_recipe_by_id(id)`, `add_recipe(data)`, `update_recipe(id, data)`, `delete_recipe(id)`。
    *   内部使用 `sqlite3` 模块连接数据库、执行 SQL 语句、处理结果。
    *   考虑定义一个简单的 `Recipe` 类或字典来表示菜谱数据。
    *   **数据库连接管理:** 确保正确处理数据库连接的打开和关闭（可以使用 Flask 的 `g` 对象和 `teardown_appcontext`）。
*   **配置 (`app/config.py`, `instance/config.py`):**
    *   `app/config.py`: 存放默认配置 (如 `DEBUG = False`, 数据库文件路径的默认值)。
    *   `instance/config.py`: 存放敏感信息或环境特定配置 (如 `SECRET_KEY`, 数据库文件实际路径)，此文件不应提交到 Git。
    *   Flask 会自动加载 `instance/config.py` (如果存在) 并覆盖 `app/config.py` 中的同名配置。
*   **测试 (`tests/`):**
    *   使用 `pytest` 和 Flask 的测试客户端 (`app.test_client()`) 编写单元测试和集成测试。
    *   测试 API 端点的响应状态码、返回数据结构和内容。
    *   测试数据访问层的功能。

## 8. 部署考虑 (简要)

*   **前端:**
    *   构建静态文件 (`npm run build` 或 `yarn build`)。
    *   部署到静态文件托管服务 (如 Netlify, Vercel, GitHub Pages) 或 Web 服务器 (Nginx, Apache)。
*   **后端:**
    *   **简单:** PythonAnywhere (易于部署 Flask 应用)。
    *   **PaaS:** Heroku, Google App Engine, Azure App Service。
    *   **VPS/服务器:** 使用 Gunicorn 或 uWSGI 作为 WSGI 服务器，Nginx 作为反向代理。
    *   需要确保服务器上有 Python 环境和 `requirements.txt` 中的依赖。
    *   SQLite 数据库文件需要与应用一起部署或放在持久化存储上。
*   **数据库:** SQLite 文件需要放置在服务器上应用可读写的位置。注意备份。
*   **CORS:** 后端需要正确配置 CORS 策略，允许来自前端域名的请求。
*   **环境变量:** 生产环境中的敏感配置（如 `SECRET_KEY`）应通过环境变量设置。

## 9. 后续步骤建议

1.  **环境搭建:**
    *   创建项目根目录。
    *   分别初始化前后端项目结构 (`frontend/`, `backend/`)。
    *   设置 Python 虚拟环境 (`backend/venv`) 并安装 `requirements.txt` (Flask, Flask-CORS)。
    *   安装 Node.js 和 npm/yarn，在 `frontend/` 目录下安装依赖 (`package.json`)。
2.  **后端开发 (API优先):**
    *   实现 Flask 应用工厂 (`create_app`)。
    *   设计并创建 SQLite 数据库表 (`recipes`)。
    *   实现数据访问层 (`app/models/recipe.py`) 的 CRUD 函数。
    *   创建 `recipes` 蓝图并实现所有 API 端点。
    *   配置 CORS。
    *   编写 API 测试 (`tests/test_recipes_api.py`)。
    *   使用 Postman 或类似工具测试 API。
3.  **前端开发:**
    *   配置 Vue Router。
    *   配置 Vuetify。
    *   实现 API 服务层 (`src/services/api.js`)。
    *   (可选) 配置 Pinia store 或创建 Composables。
    *   开发核心组件 (`RecipeCard`, `RecipeForm`, `AppHeader`)。
    *   开发页面视图 (`HomeView`, `RecipeDetailView`, `AddRecipeView`, `EditRecipeView`)。
    *   连接组件和视图到 API 服务和状态管理。
    *   实现响应式布局。
4.  **联调与测试:**
    *   同时运行前后端开发服务器。
    *   测试端到端的功能流程。
    *   修复 Bug。
5.  **完善与优化:**
    *   添加表单验证（前后端）。
    *   优化 UI/UX。
    *   添加加载指示器和错误提示。
    *   编写更多测试。
6.  **部署:**
    *   选择部署方案并进行部署。
