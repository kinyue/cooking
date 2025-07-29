# backend/app/routes/secure_recipes.py
# Secure routes for recipe management (create, update, delete)

from flask import Blueprint, jsonify, request, abort, current_app
from werkzeug.utils import secure_filename
import json
import sqlite3

# Import middleware for security
from ..middleware import local_only, token_required, secure_api_required, generate_api_token, revoke_token

# Import recipe model
from ..models import recipe as db_recipe

# Create blueprint with /api/secure prefix
bp = Blueprint('secure_recipes', __name__, url_prefix='/api/secure')

# --- Token Management Endpoints ---

@bp.route('/token', methods=['POST'])
@local_only  # Only accessible from local machine
def create_token():
    """Generate a new API token (only accessible from local machine)."""
    # Get requested expiration time from request or use default (24 hours)
    try:
        hours = request.json.get('expires_in_hours', 24)
        hours = int(hours)
        if hours <= 0 or hours > 720:  # Max 30 days
            hours = 24
    except (TypeError, ValueError):
        hours = 24
    
    token, expiration = generate_api_token(expires_in_hours=hours)
    
    return jsonify({
        "message": "API token generated successfully",
        "token": token,
        "expires_at": expiration.isoformat(),
        "expires_in_hours": hours
    }), 201

@bp.route('/token/revoke', methods=['POST'])
@local_only  # Only accessible from local machine
def revoke_token_endpoint():
    """Revoke an API token (only accessible from local machine)."""
    if not request.is_json:
        return jsonify({"message": "Request must be application/json."}), 415
    
    token = request.json.get('token')
    if not token:
        return jsonify({"message": "Token is required."}), 400
    
    success = revoke_token(token)
    if success:
        return jsonify({"message": "Token revoked successfully"}), 200
    else:
        return jsonify({"message": "Token not found or already revoked"}), 404

# --- Secure Recipe Management Endpoints ---

@bp.route('/recipes', methods=['POST'])
@secure_api_required  # Requires both local machine and valid token
def create_recipe():
    """Create a new recipe (secure endpoint)."""
    # Expect application/json
    if not request.is_json:
        return jsonify({"message": "Request must be application/json."}), 415

    request_body = request.get_json()
    if not request_body:
        return jsonify({"message": "Request body cannot be empty."}), 400

    # --- Extract recipe data ---
    # Assuming recipe data is nested under 'recipeData' key based on frontend structure
    if 'recipeData' not in request_body or not isinstance(request_body['recipeData'], dict):
         return jsonify({"message": "Missing or invalid 'recipeData' field in request body."}), 400

    recipe_data = request_body['recipeData']

    # --- Detailed Validation (applied to recipe_data regardless of source) ---
    errors = {}
    # Required fields check
    required_fields = ['name', 'ingredients', 'instructions']
    for field in required_fields:
        if field not in recipe_data:
             errors[field] = f"Missing required field: {field}"
        elif field in ['ingredients', 'instructions'] and (not isinstance(recipe_data[field], list) or not recipe_data[field]):
             errors[field] = f"Required field '{field}' must be a non-empty list."
        elif field not in ['ingredients', 'instructions'] and not recipe_data[field]: # For non-list fields like name
             errors[field] = f"Required field '{field}' cannot be empty."

    # Ingredients validation (only if field exists and basic check passed)
    if 'ingredients' not in errors and 'ingredients' in recipe_data:
        ingredient_errors = []
        for index, ingredient in enumerate(recipe_data['ingredients']):
            ing_errors = {}
            if not isinstance(ingredient, dict):
                ing_errors['general'] = f"Ingredient at index {index} must be an object."
            else:
                # Name is required for an ingredient
                if 'name' not in ingredient or not ingredient['name']:
                    ing_errors['name'] = f"Ingredient {index+1}: Name is required and cannot be empty."
                # Quantity is optional
            if ing_errors:
                ingredient_errors.append({"index": index, "errors": ing_errors})
        if ingredient_errors:
             errors['ingredients'] = ingredient_errors

    # Instructions validation (only if field exists and basic check passed)
    if 'instructions' not in errors and 'instructions' in recipe_data:
        instruction_errors = []
        for index, instruction in enumerate(recipe_data['instructions']):
            if not isinstance(instruction, str) or not instruction.strip():
                instruction_errors.append({"index": index, "error": "Instruction must be a non-empty string."})
        if instruction_errors:
             errors['instructions'] = instruction_errors

    # Optional fields validation (numeric checks if present and not None)
    numeric_fields = ['prep_time_minutes', 'cook_time_minutes', 'servings']
    for field in numeric_fields:
        # Check within recipe_data
        # Use .get() to avoid KeyError if field is missing (e.g., in JSON request)
        field_value = recipe_data.get(field)
        if field_value is not None: # Check for None explicitly, 0 is valid
            try:
                # Allow integers or floats
                val = int(field_value) if str(field_value).isdigit() else float(field_value)
                if val < 0:
                     errors[field] = f"{field.replace('_', ' ').title()} cannot be negative."
            except (ValueError, TypeError):
                errors[field] = f"{field.replace('_', ' ').title()} must be a valid number if provided."

    if errors:
        # Return structured validation errors
        # Add context that errors are within 'recipeData' if helpful
        return jsonify({"message": "Validation failed within 'recipeData'", "errors": errors}), 400

    # --- End Validation ---

    try:
        # Pass only the validated text data to the database function
        new_recipe_id = db_recipe.add_recipe(recipe_data)
        if new_recipe_id:
            # Fetch the newly created recipe
            created_recipe = db_recipe.get_recipe_by_id(new_recipe_id)
            if created_recipe:
                # Return the created recipe data
                return jsonify({
                    "message": "Recipe created successfully",
                    "data": created_recipe
                }), 201 # HTTP status code for Created
            else:
                # This case means add_recipe returned an ID, but get_recipe_by_id failed immediately after
                current_app.logger.error(f"Failed to fetch newly created recipe with ID: {new_recipe_id}")
                return jsonify({"message": "Recipe created but failed to retrieve details."}), 500
        else:
             # If add_recipe returns None/False without exception, it's an unexpected failure
             current_app.logger.error("Error creating recipe: db_recipe.add_recipe returned no ID.")
             return jsonify({"message": "Failed to create recipe due to an unknown database issue."}), 500
    except Exception as e:
        # Log the detailed error server-side
        current_app.logger.error(f"Exception during recipe creation: {e}", exc_info=True)
        error_message = str(e)
        return jsonify({"message": "Internal server error creating recipe.", "error": error_message}), 500

@bp.route('/recipes/<int:id>', methods=['PUT'])
@secure_api_required  # Requires both local machine and valid token
def update_recipe(id):
    """Update an existing recipe (secure endpoint)."""
    request_body = request.get_json()
    if not request_body:
        return jsonify({"message": "No data provided for update."}), 400

    # --- Extract recipe data ---
    # Assuming update data is also nested under 'recipeData'
    if 'recipeData' not in request_body or not isinstance(request_body['recipeData'], dict):
         return jsonify({"message": "Missing or invalid 'recipeData' field in request body."}), 400
    
    recipe_data = request_body['recipeData']
    
    # Check if recipe exists before attempting update
    existing_recipe = db_recipe.get_recipe_by_id(id)
    if existing_recipe is None:
        return jsonify({"message": f"Recipe with id {id} not found."}), 404

    # --- Detailed Validation on recipe_data (fields are optional for update) ---
    errors = {}
    # Validate fields only if they are present in the recipe_data
    if 'name' in recipe_data and not recipe_data['name']: # Name cannot be updated to empty
        errors['name'] = "Name cannot be empty."

    if 'ingredients' in recipe_data: # If ingredients are being updated
        if not isinstance(recipe_data['ingredients'], list):
             errors['ingredients'] = "Ingredients must be a list."
        elif not recipe_data['ingredients']: # Allow updating to empty list? Or require at least one?
             errors.setdefault('ingredients', []).append("Ingredients list cannot be empty if provided for update.")
        else:
            ingredient_errors = []
            for index, ingredient in enumerate(recipe_data['ingredients']):
                ing_errors = {}
                if not isinstance(ingredient, dict):
                    ing_errors['general'] = f"Ingredient at index {index} must be an object."
                else:
                    if 'name' not in ingredient or not ingredient['name']:
                        ing_errors['name'] = f"Ingredient {index+1}: Name is required and cannot be empty."
                    # Quantity is optional
                if ing_errors:
                    ingredient_errors.append({"index": index, "errors": ing_errors})
            if ingredient_errors:
                 errors['ingredients'] = ingredient_errors

    if 'instructions' in recipe_data: # If instructions are being updated
         if not isinstance(recipe_data['instructions'], list):
             errors['instructions'] = "Instructions must be a list of strings."
         elif not recipe_data['instructions']: # Allow updating to empty list?
             errors.setdefault('instructions', []).append("Instructions list cannot be empty if provided for update.")
         else:
            instruction_errors = []
            for index, instruction in enumerate(recipe_data['instructions']):
                if not isinstance(instruction, str) or not instruction.strip():
                    instruction_errors.append({"index": index, "error": "Instruction must be a non-empty string."})
            if instruction_errors:
                 errors['instructions'] = instruction_errors

    # Optional fields validation (numeric checks if present and not None)
    numeric_fields = ['prep_time_minutes', 'cook_time_minutes', 'servings']
    for field in numeric_fields:
        if field in recipe_data and recipe_data[field] is not None:
            try:
                val = float(recipe_data[field])
                if val < 0:
                     errors[field] = f"{field.replace('_', ' ').title()} cannot be negative."
            except (ValueError, TypeError):
                errors[field] = f"{field.replace('_', ' ').title()} must be a valid number if provided."

    if errors:
        return jsonify({"message": "Validation failed within 'recipeData'", "errors": errors}), 400
    # --- End Validation ---

    try:
        # Pass the validated recipe_data to the database function
        success = db_recipe.update_recipe(id, recipe_data)
        if success:
            updated_recipe = db_recipe.get_recipe_by_id(id)
            if updated_recipe:
                return jsonify({
                    "message": "Recipe updated successfully",
                    "data": updated_recipe
                })
            else:
                 # Should not happen if update reported success, but handle defensively
                 current_app.logger.error(f"Failed to fetch updated recipe with ID: {id} after successful update report.")
                 return jsonify({"message": "Recipe updated but failed to retrieve details."}), 500
        else:
            # This might happen if the update query affects 0 rows (e.g., data identical to existing)
            current_app.logger.warning(f"Update operation for recipe {id} reported no changes or failed.")
            # Fetch current data to see if it matches request or if there was another issue
            current_recipe = db_recipe.get_recipe_by_id(id)
            return jsonify({
                "message": "Recipe update operation completed, but may not have changed the record (data might be identical or another issue occurred).",
                "data": current_recipe # Return current state
                }), 200 # Return 200 OK but with a specific message
    except Exception as e:
        current_app.logger.error(f"Exception during recipe update for ID {id}: {e}", exc_info=True)
        error_message = str(e)
        return jsonify({"message": f"Internal server error updating recipe {id}.", "error": error_message}), 500

@bp.route('/recipes/<int:id>', methods=['DELETE'])
@secure_api_required  # Requires both local machine and valid token
def delete_recipe(id):
    """Delete a recipe (secure endpoint)."""
    # Check if recipe exists before attempting delete
    existing_recipe = db_recipe.get_recipe_by_id(id)
    if existing_recipe is None:
        return jsonify({"message": f"Recipe with id {id} not found."}), 404

    try:
        success = db_recipe.delete_recipe(id)
        if success:
            return jsonify({
                "message": "Recipe deleted successfully",
                "data": {"id": id}
            })
        else:
            # If delete returns False without exception
            current_app.logger.error(f"Failed to delete recipe {id}: db_recipe.delete_recipe returned False.")
            return jsonify({"message": "Failed to delete recipe due to an unknown database issue."}), 500
    except Exception as e:
        current_app.logger.error(f"Exception during recipe deletion for ID {id}: {e}", exc_info=True)
        error_message = str(e)
        return jsonify({"message": f"Internal server error deleting recipe {id}.", "error": error_message}), 500

# --- Image Upload for Secure Endpoints ---

# Define allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/recipes/<int:id>/image', methods=['POST'])
@secure_api_required  # Requires both local machine and valid token
def upload_recipe_image(id):
    """Upload an image for a specific recipe (secure endpoint)."""
    # Check if the recipe exists
    existing_recipe = db_recipe.get_recipe_by_id(id)
    if existing_recipe is None:
        return jsonify({"message": f"Recipe with id {id} not found."}), 404

    if 'image' not in request.files:
        return jsonify({"message": "No image file part in the request."}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({"message": "No selected file."}), 400

    if file and allowed_file(file.filename):
        # Read image data into memory as bytes
        image_data = file.read()

        # Basic validation: Check if image_data is not empty
        if not image_data:
             return jsonify({"message": "Uploaded file is empty."}), 400

        try:
            # Call the model function to save the image data (BLOB)
            # Get the database connection to manage the transaction
            db = db_recipe.get_db()
            image_id = db_recipe.add_recipe_image(id, image_data, alt_text=file.filename, is_primary=True)

            if image_id:
                 # Commit the transaction since add_recipe_image was successful
                 db.commit()
                 current_app.logger.info(f"Transaction committed for image upload (recipe {id}, image {image_id}).")

                 return jsonify({
                     "message": "Image uploaded successfully",
                     "data": {"recipe_id": id, "image_id": image_id}
                 }), 201
            else:
                # If add_recipe_image returns None/False without exception, rollback
                db.rollback()
                current_app.logger.error(f"Failed to save image for recipe {id}: db_recipe.add_recipe_image returned no ID. Transaction rolled back.")
                return jsonify({"message": "Failed to save image to database due to an unknown issue."}), 500

        except Exception as e:
            # Rollback the transaction on any exception during image saving
            db = db_recipe.get_db() # Ensure db is available for rollback
            db.rollback()
            current_app.logger.error(f"Exception saving image for recipe {id}: {e}. Transaction rolled back.", exc_info=True)
            error_message = str(e)
            return jsonify({"message": f"Internal server error saving image for recipe {id}.", "error": error_message}), 500

    else:
        # No database operation started, so no rollback needed here
        return jsonify({"message": f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}."}), 400