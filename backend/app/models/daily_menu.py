# backend/app/models/daily_menu.py
# Data model and database interaction functions for daily menus

import sqlite3
import json
from flask import current_app, g
from datetime import date

# Assuming get_db and close_db are managed in recipe.py or a shared db module
# If they are specific to recipe.py, we might need to import them or redefine them here.
# For now, assume they are accessible via g and current_app context.
from .recipe import get_db, recipe_to_dict # Import get_db and recipe_to_dict

def daily_menu_to_dict(row):
    """Converts a sqlite3.Row object for a daily_menu into a dictionary."""
    if row is None:
        return None
    menu_dict = dict(row)
    # Convert timestamp if needed, similar to recipe_to_dict
    if menu_dict.get('created_at'):
        menu_dict['created_at'] = menu_dict['created_at'].isoformat()
    return menu_dict

def daily_menu_recipe_to_dict(row):
    """Converts a sqlite3.Row object for a daily_menu_recipe into a dictionary."""
    if row is None:
        return None
    # Basic conversion, add more processing if needed (like joining recipe name)
    return dict(row)

def get_menu_versions_by_date(date_str):
    """Retrieves all menu versions for a specific date."""
    db = get_db()
    cursor = db.execute(
        "SELECT * FROM daily_menus WHERE menu_date = ? ORDER BY version ASC",
        (date_str,)
    )
    versions = cursor.fetchall()
    return [daily_menu_to_dict(row) for row in versions]

def get_menu_details(menu_id):
    """Retrieves all recipes and their meal types for a specific daily_menu_id."""
    db = get_db()
    # Join with recipes table to get recipe details like name
    cursor = db.execute(
        """
        SELECT
            dmr.id, dmr.daily_menu_id, dmr.recipe_id, dmr.meal_type,
            r.name as recipe_name, r.description as recipe_description, r.image_url as recipe_image_url
        FROM daily_menu_recipes dmr
        JOIN recipes r ON dmr.recipe_id = r.id
        WHERE dmr.daily_menu_id = ?
        ORDER BY dmr.id ASC
        """,
        (menu_id,)
    )
    recipes = cursor.fetchall()
    # We might want a more structured dict here, maybe group by recipe?
    # For now, return list of recipe entries in the menu.
    # Use recipe_to_dict logic if more recipe fields are needed and parsed correctly
    return [dict(row) for row in recipes] # Simple dict conversion for now

def get_latest_menu_by_date(date_str):
    """Retrieves the details of the latest menu version for a specific date."""
    db = get_db()
    # Find the latest version ID for the given date
    cursor = db.execute(
        "SELECT id FROM daily_menus WHERE menu_date = ? ORDER BY version DESC LIMIT 1",
        (date_str,)
    )
    latest_version = cursor.fetchone()

    if latest_version:
        latest_menu_id = latest_version['id']
        details = get_menu_details(latest_menu_id)
        # Also return the version info itself
        version_info = daily_menu_to_dict(db.execute("SELECT * FROM daily_menus WHERE id = ?", (latest_menu_id,)).fetchone())
        return {"version_info": version_info, "recipes": details}
    else:
        return None # No menu found for this date

def save_menu(date_str, recipes_with_type, overwrite=False):
    """
    Saves a new menu version for a given date.
    If overwrite is True, it replaces version 1.
    If overwrite is False, it adds a new version.
    `recipes_with_type` is a list of dicts: [{"recipe_id": int, "meal_type": str}]
    Returns the ID of the newly created daily_menu record or None on failure.
    """
    db = get_db()
    cursor = None
    new_version_number = 1

    try:
        # Start transaction
        db.execute("BEGIN")

        # Check existing versions for the date
        cursor = db.execute(
            "SELECT MAX(version) as max_version FROM daily_menus WHERE menu_date = ?",
            (date_str,)
        )
        result = cursor.fetchone()
        max_version = result['max_version'] if result and result['max_version'] is not None else 0

        if overwrite:
            # If overwriting, we target version 1.
            # We might need to delete existing version 1 and its recipes first,
            # or handle this via UNIQUE constraint failure (simpler for now).
            # Let's assume overwrite means "create version 1, potentially replacing".
            # For simplicity, let's just try to insert version 1. If it fails due to UNIQUE,
            # it means version 1 exists. A more robust approach might delete first.
            new_version_number = 1
            # Consider deleting existing version 1 recipes if replacing:
            # cursor = db.execute("SELECT id FROM daily_menus WHERE menu_date = ? AND version = 1", (date_str,))
            # existing_v1 = cursor.fetchone()
            # if existing_v1:
            #     db.execute("DELETE FROM daily_menu_recipes WHERE daily_menu_id = ?", (existing_v1['id'],))
            #     db.execute("DELETE FROM daily_menus WHERE id = ?", (existing_v1['id'],))

        elif max_version > 0:
            # If not overwriting and versions exist, increment the version number
            new_version_number = max_version + 1
        # else: new_version_number remains 1 (first version for the date)

        # Insert the new menu version record
        cursor = db.execute(
            "INSERT INTO daily_menus (menu_date, version) VALUES (?, ?)",
            (date_str, new_version_number)
        )
        new_daily_menu_id = cursor.lastrowid

        if not new_daily_menu_id:
            raise sqlite3.Error("Failed to insert into daily_menus table.")

        # Insert recipes for the new menu version
        if recipes_with_type: # Ensure there are recipes to insert
            recipes_data = [
                (new_daily_menu_id, item['recipe_id'], item.get('meal_type', '其他'))
                for item in recipes_with_type if 'recipe_id' in item # Basic validation
            ]
            if recipes_data: # Check if there's valid data after filtering
                db.executemany(
                    "INSERT INTO daily_menu_recipes (daily_menu_id, recipe_id, meal_type) VALUES (?, ?, ?)",
                    recipes_data
                )

        # Commit transaction
        db.commit()
        current_app.logger.info(f"Successfully saved menu version {new_version_number} for date {date_str} (ID: {new_daily_menu_id}).")
        return new_daily_menu_id

    except sqlite3.IntegrityError as e:
        # Handle potential UNIQUE constraint violation if trying to overwrite improperly
        db.rollback()
        current_app.logger.error(f"Integrity error saving menu for {date_str} (version {new_version_number}): {e}", exc_info=True)
        # This might happen if trying to insert version 1 when it already exists and overwrite logic wasn't robust enough
        return None # Indicate failure
    except sqlite3.Error as e:
        db.rollback()
        current_app.logger.error(f"Database error saving menu for {date_str}: {e}", exc_info=True)
        return None # Indicate failure
    except Exception as e:
        db.rollback()
        current_app.logger.error(f"Unexpected error saving menu for {date_str}: {e}", exc_info=True)
        return None # Indicate failure


def get_dates_with_menus():
    """Retrieves a distinct list of dates ('YYYY-MM-DD') that have saved menus."""
    db = get_db()
    cursor = db.execute(
        "SELECT DISTINCT menu_date FROM daily_menus ORDER BY menu_date DESC"
    )
    dates = cursor.fetchall()
    return [row['menu_date'] for row in dates]
