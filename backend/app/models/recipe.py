# backend/app/models/recipe.py
# Recipe data model and database interaction functions
import sqlite3
import json
from flask import current_app, g

def get_db():
    """Connects to the specific database."""
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row # Return rows that behave like dicts
    return g.db

def close_db(e=None):
    """Closes the database connection."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Clear existing data and create new tables."""
    db_path = current_app.config['DATABASE']
    print(f"Attempting to initialize database at: {db_path}") # Add print statement
    db = get_db()
    # Read the schema file
    # Assuming schema.sql is in the same directory or accessible path
    # For simplicity now, embedding the schema directly.
    # In a real app, load from a file:
    # with current_app.open_resource('schema.sql') as f:
    #     db.executescript(f.read().decode('utf8'))

    schema = """
    DROP TABLE IF EXISTS recipes;

    CREATE TABLE recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        ingredients TEXT NOT NULL, -- Storing as JSON string
        instructions TEXT NOT NULL, -- Storing as JSON string
        image_url TEXT,
        tags TEXT, -- Storing as JSON string '["tag1", "tag2"]'
        difficulty TEXT,
        cuisine TEXT,
        prep_time_minutes INTEGER,
        cook_time_minutes INTEGER,
        servings INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TRIGGER IF NOT EXISTS update_recipes_updated_at
    AFTER UPDATE ON recipes
    FOR EACH ROW
    BEGIN
        UPDATE recipes SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
    END;

    CREATE INDEX IF NOT EXISTS idx_recipes_name ON recipes (name);
    -- Indexing JSON tags might require specific SQLite JSON functions if complex queries are needed
    -- CREATE INDEX IF NOT EXISTS idx_recipes_tags ON recipes (json_extract(tags, '$'));
    """
    db.executescript(schema)
    print("Initialized the recipes table.")

    # Initialize the recipe_images table from its schema file
    try:
        # Assuming open_resource looks relative to the application root or blueprint location
        # Adjust path if needed, e.g., 'data/schema_images.sql' if relative to project root
        with current_app.open_resource('../data/schema_images.sql') as f:
              images_schema = f.read().decode('utf8')
              db.executescript(images_schema)
        print("Initialized the recipe_images table.")
    except FileNotFoundError:
         print("Error: Could not find schema_images.sql. Make sure it's in the backend/data directory.")
    except Exception as e:
         print(f"Error initializing recipe_images table: {e}")

    # Initialize the daily menu tables from its schema file
    try:
        with current_app.open_resource('../data/schema_daily_menus.sql') as f:
            daily_menus_schema = f.read().decode('utf8') # Corrected indentation
            db.executescript(daily_menus_schema) # Corrected indentation
        print("Initialized the daily_menus and daily_menu_recipes tables.")
    except FileNotFoundError:
        print("Error: Could not find schema_daily_menus.sql. Make sure it's in the backend/data directory.")
    except Exception as e:
        print(f"Error initializing daily_menu tables: {e}") # Corrected error message context


def init_app(app):
    """Register database functions with the Flask app."""
    app.teardown_appcontext(close_db)
    # Note: All CLI command registrations moved to app factory (__init__.py)


# --- CRUD Operations ---

def recipe_to_dict(row):
    """Converts a sqlite3.Row object into a dictionary, parsing JSON fields."""
    if row is None:
        return None
    recipe_dict = dict(row)
    try:
        recipe_dict['ingredients'] = json.loads(recipe_dict['ingredients'])
    except (json.JSONDecodeError, TypeError):
        recipe_dict['ingredients'] = [] # Or handle error as appropriate
    try:
        recipe_dict['instructions'] = json.loads(recipe_dict['instructions'])
    except (json.JSONDecodeError, TypeError):
        recipe_dict['instructions'] = []
    try:
        recipe_dict['tags'] = json.loads(recipe_dict['tags'])
    except (json.JSONDecodeError, TypeError):
         recipe_dict['tags'] = [] # Or handle error as appropriate
    # Convert timestamps to ISO format string for JSON serialization
    if recipe_dict.get('created_at'):
        recipe_dict['created_at'] = recipe_dict['created_at'].isoformat()
    if recipe_dict.get('updated_at'):
        recipe_dict['updated_at'] = recipe_dict['updated_at'].isoformat()
    return recipe_dict

def get_all_recipes(filters=None, page=1, limit=8):
    """Retrieves recipes with filtering and pagination."""
    db = get_db()
    base_query = "FROM recipes"
    count_query = "SELECT COUNT(*) " + base_query
    select_query = "SELECT * " + base_query
    params = []
    count_params = [] # Separate params for count query if needed

    # --- Filtering ---
    where_clauses = []
    if filters:
        # 搜索条件
        if filters.get('search'):
            where_clauses.append("(name LIKE ? OR description LIKE ?)")
            term = f"%{filters['search']}%"
            params.extend([term, term])
            count_params.extend([term, term])

        # 食材筛选 (逗号分隔的字符串)
        if filters.get('ingredients'):
            ingredient_terms = [term.strip() for term in filters['ingredients'].split(',') if term.strip()]
            if ingredient_terms:
                ingredient_conditions = []
                for term in ingredient_terms:
                    # Search for the ingredient name within the JSON string
                    # This assumes ingredients are stored like: '[{"name": "鸡蛋", ...}, {"name": "番茄", ...}]'
                    ingredient_conditions.append("ingredients LIKE ?")
                    param = f'%"{term}"%' # Basic search for the ingredient name as a string literal within the JSON
                    params.append(param)
                    count_params.append(param)
                # Require ALL ingredients to be present
                where_clauses.append(f"({' AND '.join(ingredient_conditions)})")

        # 标签筛选 (Revised using JSON functions)
        tags_filter = filters.get('tags')
        if tags_filter: # Check for non-None AND non-empty list
            # filters['tags'] is a non-empty list of tags like ['tag1', 'tag2']
            tag_conditions = []
            for tag in tags_filter:
                # Use json_each to check if the tag exists in the JSON array 'tags'
                # This finds recipes where *any* of the provided tags match.
                tag_conditions.append("EXISTS (SELECT 1 FROM json_each(recipes.tags) WHERE json_each.value = ?)")
                params.append(tag.strip()) # Add the tag itself as a parameter
                count_params.append(tag.strip())
            if tag_conditions:
                # Combine conditions with OR: find recipes matching *any* of the tags
                current_app.logger.debug(f"Tag Condition: {tag_conditions}") 
                where_clauses.append(f"({' OR '.join(tag_conditions)})")

        # 难度筛选
        if filters.get('difficulty'):
            where_clauses.append("difficulty = ?")
            params.append(filters['difficulty'])
            count_params.append(filters['difficulty'])

        # 菜系筛选
        if filters.get('cuisine'):
            where_clauses.append("cuisine = ?")
            params.append(filters['cuisine'])
            count_params.append(filters['cuisine'])

        # 准备时间范围
        if filters.get('prep_time_min') is not None:
            where_clauses.append("prep_time_minutes >= ?")
            params.append(filters['prep_time_min'])
            count_params.append(filters['prep_time_min'])
        if filters.get('prep_time_max') is not None:
            where_clauses.append("prep_time_minutes <= ?")
            params.append(filters['prep_time_max'])
            count_params.append(filters['prep_time_max'])

        # 烹饪时间范围
        if filters.get('cook_time_min') is not None:
            where_clauses.append("cook_time_minutes >= ?")
            params.append(filters['cook_time_min'])
            count_params.append(filters['cook_time_min'])
        if filters.get('cook_time_max') is not None:
            where_clauses.append("cook_time_minutes <= ?")
            params.append(filters['cook_time_max'])
            count_params.append(filters['cook_time_max'])

        # 份量范围
        if filters.get('servings_min') is not None:
            where_clauses.append("servings >= ?")
            params.append(filters['servings_min'])
            count_params.append(filters['servings_min'])
        if filters.get('servings_max') is not None:
            where_clauses.append("servings <= ?")
            params.append(filters['servings_max'])
            count_params.append(filters['servings_max'])

    if where_clauses:
        where_sql = " WHERE " + " AND ".join(where_clauses)
        count_query += where_sql
        select_query += where_sql

    # --- Get Total Count ---
    count_cursor = db.execute(count_query, count_params)
    total_items = count_cursor.fetchone()[0]

    # --- Ordering ---
    sort_by = filters.get('sort', 'created_at') if filters else 'created_at'
    order = filters.get('order', 'desc').lower() if filters else 'desc'
    if sort_by in ['name', 'created_at', 'updated_at', 'difficulty'] and order in ['asc', 'desc']:
         select_query += f" ORDER BY {sort_by} {order.upper()}"
    else:
        select_query += " ORDER BY created_at DESC" # Default sort

    # --- Pagination ---
    offset = (page - 1) * limit
    select_query += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    # --- Fetch Recipes for the Page ---
    cursor = db.execute(select_query, params)
    recipes_page = cursor.fetchall()

    # Return page data and total count
    return ([recipe_to_dict(row) for row in recipes_page], total_items)


def get_recipe_by_id(recipe_id):
    """Retrieves a single recipe by its ID."""
    db = get_db()
    cursor = db.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
    recipe = cursor.fetchone()
    return recipe_to_dict(recipe)


def get_random_recipes(count=3):
    """Retrieves a specified number of random recipes."""
    db = get_db()
    # Ensure count is a positive integer
    try:
        limit = int(count)
        if limit <= 0:
            limit = 3 # Default to 3 if invalid count provided
    except (ValueError, TypeError):
        limit = 3 # Default to 3 if conversion fails

    # SQLite uses RANDOM() for random ordering
    cursor = db.execute("SELECT * FROM recipes ORDER BY RANDOM() LIMIT ?", (limit,))
    recipes = cursor.fetchall()
    return [recipe_to_dict(row) for row in recipes]


def add_recipe(data):
    """Adds a new recipe (text data only) to the database."""
    db = get_db()
    # Image data is handled by add_recipe_image, not here.

    # Prepare data for the recipes table.
    # Include image_url if it's provided as part of the text data (e.g., external URL)
    # Otherwise, it will be NULL initially.
    # Corrected tuple to match the 11 columns in the INSERT statement
    recipe_data_tuple = (
        data.get('name'),                       # 1. name
        data.get('description'),                # 2. description
        json.dumps(data.get('ingredients', [])), # 3. ingredients
        json.dumps(data.get('instructions', [])),# 4. instructions
        data.get('image_url'),                  # 5. image_url
        json.dumps(data.get('tags', [])),       # 6. tags
        data.get('difficulty'),                 # 7. difficulty
        data.get('cuisine'),                    # 8. cuisine
        data.get('prep_time_minutes'),          # 9. prep_time_minutes
        data.get('cook_time_minutes'),          # 10. cook_time_minutes
        data.get('servings')                    # 11. servings
    )

    cursor = None
    try:
        # Insert recipe text data
        cursor = db.execute(
            """
            INSERT INTO recipes (name, description, ingredients, instructions, image_url, tags, difficulty, cuisine, prep_time_minutes, cook_time_minutes, servings)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            recipe_data_tuple
        )
        db.commit()
        new_recipe_id = cursor.lastrowid
        current_app.logger.info(f"Successfully added recipe text data (ID: {new_recipe_id}).")
        return new_recipe_id # Return the ID of the newly inserted recipe

    except sqlite3.Error as e:
        # Use Flask logger for better visibility
        current_app.logger.error(f"Database error in add_recipe (text data): {e}", exc_info=True)
        if db:
            db.rollback() # Rollback transaction on any database error
        raise e # Re-raise to be caught by the route handler
    except Exception as e:
        # Catch other potential errors
        current_app.logger.error(f"Unexpected error in add_recipe (text data): {e}", exc_info=True)
        if db:
            db.rollback() # Rollback transaction
        raise e # Re-raise to be caught by the route handler


def update_recipe(recipe_id, data):
    """Updates an existing recipe."""
    db = get_db()
    # Construct the SET part of the query dynamically based on provided data
    set_clause = []
    params = []
    allowed_fields = ['name', 'description', 'ingredients', 'instructions', 'image_url', 'tags', 'difficulty', 'cuisine', 'prep_time_minutes', 'cook_time_minutes', 'servings']

    for field in allowed_fields:
        if field in data:
            set_clause.append(f"{field} = ?")
            value = data[field]
            # Ensure complex fields are stored as JSON strings
            if field in ['ingredients', 'instructions', 'tags']:
                value = json.dumps(value)
            params.append(value)

    if not set_clause:
        return False # Nothing to update

    params.append(recipe_id)
    # Rely on the database trigger to update updated_at
    query = f"UPDATE recipes SET {', '.join(set_clause)} WHERE id = ?"

    cursor = db.execute(query, params)
    db.commit()
    return cursor.rowcount > 0 # Return True if a row was updated


def delete_recipe(recipe_id):
    """Deletes a recipe from the database."""
    db = get_db()
    cursor = db.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    db.commit()
    return cursor.rowcount > 0 # Return True if a row was deleted


def get_recipe_primary_image_data(recipe_id):
    """Retrieves the primary image data (BLOB) for a given recipe ID."""
    db = get_db()
    cursor = db.execute(
        "SELECT image_data FROM recipe_images WHERE recipe_id = ? AND is_primary = 1",
        (recipe_id,)
    )
    image_row = cursor.fetchone()
    if image_row and image_row['image_data']:
        return image_row['image_data']
    else:
        return None


def add_recipe_image(recipe_id, image_data, alt_text=None, is_primary=True):
    """
    Adds an image to the recipe_images table for a specific recipe.
    If is_primary is True, it first sets any existing primary image for that recipe to not primary.
    """
    """
    Adds an image to the recipe_images table for a specific recipe.
    If is_primary is True, it first sets any existing primary image for that recipe to not primary.
    NOTE: This function now assumes it's called within an existing transaction
          managed by the caller (e.g., add_recipe). It does not manage its own transaction.
    """
    db = get_db() # Get the connection (which should be in a transaction state)
    cursor = None
    # Removed try/except block and transaction management from here.
    # Errors will propagate up to the caller (add_recipe) to handle rollback.

    # If this image is intended to be the primary one, unset other primary images for this recipe first
    if is_primary:
            db.execute(
                "UPDATE recipe_images SET is_primary = 0 WHERE recipe_id = ? AND is_primary = 1",
                (recipe_id,)
            )

    # Insert the new image record (Corrected indentation)
    cursor = db.execute(
        """
        INSERT INTO recipe_images (recipe_id, image_data, alt_text, is_primary)
            VALUES (?, ?, ?, ?)
            """,
            (
                recipe_id,
                sqlite3.Binary(image_data), # Ensure data is treated as BLOB
                alt_text,
                1 if is_primary else 0
            )
        )
    # Removed commit and rollback logic from here.
    # Let the caller (add_recipe) handle commit/rollback for the entire operation.
    # Errors will propagate up.
    new_image_id = cursor.lastrowid if cursor else None
    if new_image_id:
        current_app.logger.info(f"Successfully added image (ID: {new_image_id}) for recipe {recipe_id}.")
    else:
        # This case might indicate an issue even without an exception, log it.
        current_app.logger.warning(f"add_recipe_image for recipe {recipe_id} executed but did not return a lastrowid.")
    return new_image_id


# --- No CLI Commands in this file ---
# All CLI commands have been moved to cli_commands.py
