# backend/app/routes/daily_menus.py
# Routes for daily menu related operations

from flask import Blueprint, jsonify, request, abort, current_app
from datetime import datetime
from ..models import daily_menu as db_daily_menu # Import the new model functions

bp = Blueprint('daily_menus', __name__, url_prefix='/api/daily-menus')

# Helper function to validate date format
def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

@bp.route('/', methods=['GET'], strict_slashes=False) # Allow access without trailing slash
def get_daily_menu():
    """
    Get the latest menu details and all available versions for a specific date.
    Requires 'date' query parameter in 'YYYY-MM-DD' format.
    """
    date_str = request.args.get('date')
    if not date_str:
        return jsonify({"message": "Missing 'date' query parameter."}), 400
    if not validate_date(date_str):
        return jsonify({"message": "Invalid date format. Please use YYYY-MM-DD."}), 400

    try:
        latest_menu = db_daily_menu.get_latest_menu_by_date(date_str)
        versions = db_daily_menu.get_menu_versions_by_date(date_str)

        # latest_menu will be None if no menu exists for the date
        # versions will be an empty list if no menu exists

        return jsonify({
            "latest_menu": latest_menu, # Contains {'version_info': {...}, 'recipes': [...]} or None
            "versions": versions        # List of {'id': ..., 'menu_date': ..., 'version': ..., 'created_at': ...}
        })
    except Exception as e:
        current_app.logger.error(f"Error fetching daily menu for date {date_str}: {e}", exc_info=True)
        abort(500, description=f"Internal server error fetching menu for date {date_str}.")


@bp.route('/dates', methods=['GET'])
def get_menu_dates():
    """Get a list of all dates that have at least one saved menu."""
    try:
        dates = db_daily_menu.get_dates_with_menus()
        return jsonify({"dates": dates})
    except Exception as e:
        current_app.logger.error(f"Error fetching dates with menus: {e}", exc_info=True)
        abort(500, description="Internal server error fetching menu dates.")


# New route to get dates with menus within a specific month
@bp.route('/dates-in-month', methods=['GET'])
def get_menu_dates_in_month():
    """
    Get a list of dates within a specific year and month that have saved menus.
    Requires 'year' and 'month' query parameters (integers).
    """
    year_str = request.args.get('year')
    month_str = request.args.get('month')

    if not year_str or not month_str:
        return jsonify({"message": "Missing 'year' or 'month' query parameter."}), 400

    try:
        year = int(year_str)
        month = int(month_str)
        # Basic validation for month range
        if not (1 <= month <= 12):
             raise ValueError("Month must be between 1 and 12.")
        # Basic validation for year (optional, adjust range as needed)
        if not (1900 <= year <= 2100):
             raise ValueError("Year seems out of reasonable range.")

    except ValueError as e:
        return jsonify({"message": f"Invalid year or month parameter: {e}"}), 400

    try:
        # Call a new model function to get dates for the specific month
        # We will need to implement get_dates_with_menus_in_month in the model
        dates = db_daily_menu.get_dates_with_menus_in_month(year, month)
        return jsonify({"dates": dates})
    except Exception as e:
        current_app.logger.error(f"Error fetching menu dates for {year}-{month}: {e}", exc_info=True)
        abort(500, description=f"Internal server error fetching menu dates for {year}-{month}.")


@bp.route('/', methods=['POST'], strict_slashes=False) # Allow access without trailing slash
def save_daily_menu():
    """
    Save a new menu version for a specific date.
    Requires 'date' query parameter ('YYYY-MM-DD').
    Requires JSON body with 'recipes': [{"recipe_id": int, "meal_type": str}].
    Optional 'overwrite' query parameter (boolean, default false).
    """
    date_str = request.args.get('date')
    overwrite_str = request.args.get('overwrite', 'false').lower() # Default to 'false'

    if not date_str:
        return jsonify({"message": "Missing 'date' query parameter."}), 400
    if not validate_date(date_str):
        return jsonify({"message": "Invalid date format. Please use YYYY-MM-DD."}), 400

    if overwrite_str not in ['true', 'false']:
        return jsonify({"message": "Invalid 'overwrite' parameter. Use 'true' or 'false'."}), 400
    overwrite = overwrite_str == 'true'

    if not request.is_json:
        return jsonify({"message": "Request must be application/json."}), 415

    request_body = request.get_json()
    if not request_body or 'recipes' not in request_body:
        return jsonify({"message": "Missing 'recipes' field in request body."}), 400

    recipes_data = request_body['recipes']
    if not isinstance(recipes_data, list):
         return jsonify({"message": "'recipes' field must be a list."}), 400

    # Basic validation for recipe items in the list
    validated_recipes = []
    for item in recipes_data:
        if isinstance(item, dict) and 'recipe_id' in item and isinstance(item['recipe_id'], int):
            validated_recipes.append({
                "recipe_id": item['recipe_id'],
                "meal_type": item.get('meal_type', '其他') # Use default if missing
            })
        else:
            # Log invalid item structure if needed
            pass # Skip invalid items or return error? For now, skip.

    if not validated_recipes and recipes_data:
         return jsonify({"message": "No valid recipe data found in 'recipes' list. Each item needs at least 'recipe_id' (integer)."}), 400
    # Allow saving an empty menu? If yes, validated_recipes can be empty. If not, add check here.
    # if not validated_recipes:
    #     return jsonify({"message": "Cannot save an empty menu."}), 400

    try:
        # Call the model function to save the menu
        new_menu_id = db_daily_menu.save_menu(date_str, validated_recipes, overwrite)

        if new_menu_id:
            # Fetch the newly created/updated menu details to return
            # If overwriting, latest might be the one we just created (version 1)
            # If adding new version, latest will be the one we just created
            saved_menu_details = db_daily_menu.get_latest_menu_by_date(date_str) # This gets the *latest*, which should be the one just saved
            return jsonify({
                "message": "Menu saved successfully.",
                "new_menu_id": new_menu_id,
                "saved_menu": saved_menu_details # Return the saved menu details
            }), 201 # HTTP status code for Created
        else:
            # save_menu returned None, indicating failure (e.g., integrity error, db error)
            # Check if it was an integrity error (likely trying to overwrite version 1 when overwrite=false)
            # More specific error handling could be added here based on why save_menu failed
             return jsonify({"message": "Failed to save menu. Possible reasons: database error, or trying to overwrite version 1 without 'overwrite=true'."}), 500

    except Exception as e:
        current_app.logger.error(f"Exception saving daily menu for date {date_str}: {e}", exc_info=True)
        abort(500, description=f"Internal server error saving menu for date {date_str}.")


# Optional: Endpoint to get a specific menu version by its ID
@bp.route('/<int:menu_id>', methods=['GET'])
def get_specific_menu_version(menu_id):
    """Get the details of a specific menu version by its daily_menu_id."""
    try:
        menu_details = db_daily_menu.get_menu_details(menu_id)
        if not menu_details:
            # If details are empty, check if the menu_id itself exists
            version_info = db_daily_menu.daily_menu_to_dict(
                db_daily_menu.get_db().execute("SELECT * FROM daily_menus WHERE id = ?", (menu_id,)).fetchone()
            )
            if version_info:
                 # Menu version exists but has no recipes (maybe saved empty?)
                 return jsonify({"version_info": version_info, "recipes": []})
            else:
                 abort(404, description=f"Menu version with id {menu_id} not found.")

        # Need version info as well
        version_info = db_daily_menu.daily_menu_to_dict(
             db_daily_menu.get_db().execute("SELECT * FROM daily_menus WHERE id = ?", (menu_id,)).fetchone()
        )
        return jsonify({"version_info": version_info, "recipes": menu_details})

    except Exception as e:
        current_app.logger.error(f"Error fetching menu version id {menu_id}: {e}", exc_info=True)
        abort(500, description=f"Internal server error fetching menu version {menu_id}.")
