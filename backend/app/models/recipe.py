# backend/app/models/recipe.py
# Recipe data model and database interaction functions
import sqlite3
import json
import click # Import click for CLI commands
from flask import current_app, g
from flask.cli import with_appcontext # Helper for CLI commands

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
    print("Initialized the database.")


def init_app(app):
    """Register database functions with the Flask app."""
    app.teardown_appcontext(close_db)
    # Register the init-db command
    app.cli.add_command(init_db_command)


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
        if filters.get('search'):
            where_clauses.append("(name LIKE ? OR description LIKE ?)")
            term = f"%{filters['search']}%"
            params.extend([term, term])
            count_params.extend([term, term]) # Add to count params as well
        # TODO: Add more filters for tags, difficulty, cuisine etc.
        # Example for tags (simple LIKE, might be slow):
        # if filters.get('tags'):
        #     tag_list = filters['tags'].split(',') # Assuming comma-separated
        #     for tag in tag_list:
        #         where_clauses.append("tags LIKE ?")
        #         params.append(f'%"{tag.strip()}"%') # Search within JSON array string
        #         count_params.append(f'%"{tag.strip()}"%')

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


def add_recipe(data):
    """Adds a new recipe to the database."""
    db = get_db()
    cursor = db.execute(
        """
        INSERT INTO recipes (name, description, ingredients, instructions, image_url, tags, difficulty, cuisine, prep_time_minutes, cook_time_minutes, servings)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data.get('name'),
            data.get('description'),
            json.dumps(data.get('ingredients', [])), # Ensure JSON format
            json.dumps(data.get('instructions', [])), # Ensure JSON format
            data.get('image_url'),
            json.dumps(data.get('tags', [])), # Ensure JSON format
            data.get('difficulty'),
            data.get('cuisine'),
            data.get('prep_time_minutes'),
            data.get('cook_time_minutes'),
            data.get('servings')
        )
    )
    db.commit()
    return cursor.lastrowid # Return the ID of the newly inserted recipe


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
    query = f"UPDATE recipes SET {', '.join(set_clause)}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"

    cursor = db.execute(query, params)
    db.commit()
    return cursor.rowcount > 0 # Return True if a row was updated


def delete_recipe(recipe_id):
    """Deletes a recipe from the database."""
    db = get_db()
    cursor = db.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    db.commit()
    return cursor.rowcount > 0 # Return True if a row was deleted


# --- CLI Command ---

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
