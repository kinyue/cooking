-- SQL schema for the recipe_images table
-- This table stores image information related to recipes.

CREATE TABLE IF NOT EXISTS recipe_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL,
    image_data BLOB NOT NULL, -- Changed from image_url TEXT to store image data directly
    alt_text TEXT,
    is_primary INTEGER DEFAULT 0 CHECK(is_primary IN (0, 1)), -- Ensure only 0 or 1
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);

-- Optional: Add an index for faster lookups by recipe_id
CREATE INDEX IF NOT EXISTS idx_recipe_images_recipe_id ON recipe_images(recipe_id);

-- Optional: Add a unique constraint if you want only one primary image per recipe
-- CREATE UNIQUE INDEX IF NOT EXISTS idx_recipe_images_primary ON recipe_images(recipe_id) WHERE is_primary = 1;
-- Note: SQLite versions before 3.8.0 might not support partial indexes like the one above.
-- If compatibility with older SQLite is needed, this logic might need to be enforced at the application level.
