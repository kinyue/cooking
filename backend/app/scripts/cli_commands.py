# backend/app/scripts/cli_commands.py
# Central location for all Flask CLI commands related to database operations
import os
import sqlite3
import click
from flask import current_app
from flask.cli import with_appcontext
# Import database functions from the models module
from ..models.recipe import get_db, close_db, init_db

# Define the path to the image file relative to the project root (backend folder)
# Go up two levels from scripts to backend, then down to data/seed_images
IMAGE_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'seed_images', 'Gemini_Generated_Image_7pdmoi7pdmoi7pdm.jpg')

def seed_recipe_images():
    """Seeds the recipe_images table with a default image for all existing recipes."""
    db = get_db()
    image_data = None
    recipe_ids = []

    # 1. Read the image file
    try:
        with open(IMAGE_FILE_PATH, 'rb') as f:
            image_data = f.read()
        print(f"Successfully read image file: {IMAGE_FILE_PATH}")
    except FileNotFoundError:
        print(f"Error: Image file not found at {IMAGE_FILE_PATH}. Cannot seed images.")
        return
    except Exception as e:
        print(f"Error reading image file: {e}")
        return

    if not image_data:
        print("Error: Image data is empty. Cannot seed images.")
        return

    # 2. Get all recipe IDs
    try:
        cursor = db.execute("SELECT id FROM recipes")
        rows = cursor.fetchall()
        recipe_ids = [row['id'] for row in rows]
        if not recipe_ids:
            print("No recipes found in the database. Skipping image seeding.")
            return
        print(f"Found {len(recipe_ids)} recipes to add images for.")
    except Exception as e:
        print(f"Error fetching recipe IDs: {e}")
        return

    # 3. Insert image data for each recipe
    inserted_count = 0
    skipped_count = 0
    for recipe_id in recipe_ids:
        try:
            # Check if an image already exists for this recipe_id to avoid duplicates
            # (Optional, but good practice if the script might be run multiple times)
            cursor = db.execute("SELECT 1 FROM recipe_images WHERE recipe_id = ?", (recipe_id,))
            if cursor.fetchone():
                print(f"Image already exists for recipe_id {recipe_id}. Skipping.")
                skipped_count += 1
                continue

            # Insert the image data
            alt_text = f"Image for recipe {recipe_id}" # Basic alt text
            is_primary = 1 # Assume this is the primary image
            db.execute(
                """
                INSERT INTO recipe_images (recipe_id, image_data, alt_text, is_primary)
                VALUES (?, ?, ?, ?)
                """,
                (recipe_id, image_data, alt_text, is_primary)
            )
            inserted_count += 1
        except sqlite3.IntegrityError as e:
             print(f"Integrity error inserting image for recipe_id {recipe_id}: {e}. Skipping.")
             skipped_count += 1
        except Exception as e:
            print(f"Error inserting image for recipe_id {recipe_id}: {e}. Skipping.")
            skipped_count += 1 # Count as skipped if error occurs

    # 4. Commit changes
    if inserted_count > 0:
        try:
            db.commit()
            print(f"Successfully inserted {inserted_count} images.")
        except Exception as e:
            print(f"Error committing changes: {e}")
            # Consider rolling back if needed, though individual errors were skipped
    else:
        print("No new images were inserted.")

    if skipped_count > 0:
        print(f"Skipped inserting images for {skipped_count} recipes (already existed or error).")


    # 5. Close the database connection
    close_db()


def seed_recipes():
    """Seeds the recipes table from seed_data.sql."""
    db = get_db()
    # Construct a more reliable path to seed_data.sql
    # Go up two levels from scripts to backend, then down to data
    seed_data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'seed_data.sql')
    try:
        with open(seed_data_path, 'r', encoding='utf-8') as f:
            seed_sql = f.read()
            db.executescript(seed_sql)
        print(f"Executed seed_data.sql successfully from {seed_data_path}.")
    except FileNotFoundError:
        print(f"Error: Could not find seed_data.sql at {seed_data_path}. Make sure it's in the backend/data directory.")
    except Exception as e:
        print(f"Error executing seed_data.sql: {e}")


# CLI Commands
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    print("Starting database initialization...")
    init_db()
    print("Database initialization finished.")


@click.command('seed-recipes')
@with_appcontext
def seed_recipes_command():
    """Seeds the recipes table with sample data."""
    print("Starting recipe seeding process...")
    seed_recipes()
    print("Recipe seeding process finished.")


@click.command('seed-images')
@with_appcontext
def seed_images_command():
    """Seeds the recipe_images table with a default image."""
    print("Starting image seeding process...")
    seed_recipe_images()
    print("Image seeding process finished.")
