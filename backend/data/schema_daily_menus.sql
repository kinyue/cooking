-- Schema for daily menu tables

-- Table to store basic menu information (date, version)
CREATE TABLE IF NOT EXISTS daily_menus (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    menu_date TEXT NOT NULL, -- Store date as 'YYYY-MM-DD'
    version INTEGER NOT NULL, -- Version number for the menu on that date, starting from 1
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(menu_date, version) -- Ensure uniqueness for a given date and version
);

-- Index for faster date lookups
CREATE INDEX IF NOT EXISTS idx_daily_menus_date ON daily_menus (menu_date);

-- Table to store recipes included in a specific menu version and their meal type
CREATE TABLE IF NOT EXISTS daily_menu_recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    daily_menu_id INTEGER NOT NULL, -- Foreign key referencing daily_menus.id
    recipe_id INTEGER NOT NULL,     -- Foreign key referencing recipes.id
    meal_type TEXT CHECK(meal_type IN ('早餐', '午餐', '晚餐', '夜宵', '小吃', '其他')) DEFAULT '其他', -- Recipe classification
    FOREIGN KEY (daily_menu_id) REFERENCES daily_menus (id) ON DELETE CASCADE, -- Cascade delete if a menu version is removed
    FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON DELETE CASCADE -- Cascade delete if a recipe is removed (consider if this is desired)
);

-- Indexes for faster lookups based on menu or recipe
CREATE INDEX IF NOT EXISTS idx_daily_menu_recipes_menu_id ON daily_menu_recipes (daily_menu_id);
CREATE INDEX IF NOT EXISTS idx_daily_menu_recipes_recipe_id ON daily_menu_recipes (recipe_id);
