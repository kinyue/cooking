# backend/app/routes/recipes.py
# Routes for recipe related operations
import os
from flask import Blueprint, jsonify, request, abort, current_app
from werkzeug.utils import secure_filename
# Import specific functions for clarity or keep as is
from ..models import recipe as db_recipe

bp = Blueprint('recipes', __name__, url_prefix='/api/recipes')
limit_per_page = 8 # Default limit for pagination

@bp.route('/', methods=['GET'])
def get_recipes():
    """Get a list of recipes, potentially filtered."""
    # Extract filter parameters from request query string
    filters = {
        'search': request.args.get('search'),
        'ingredients': request.args.get('ingredients'), # Add ingredients filter
        'tags': request.args.getlist('tags') if 'tags' in request.args else None, # Use getlist to handle multiple tags
        'difficulty': request.args.get('difficulty'),
        'cuisine': request.args.get('cuisine'),
        'prep_time_min': request.args.get('prepTimeMin', type=int),
        'prep_time_max': request.args.get('prepTimeMax', type=int),
        'cook_time_min': request.args.get('cookTimeMin', type=int),
        'cook_time_max': request.args.get('cookTimeMax', type=int),
        'servings_min': request.args.get('servingsMin', type=int),
        'servings_max': request.args.get('servingsMax', type=int),
        'sort': request.args.get('sort'),
        'order': request.args.get('order'),
        'page': request.args.get('page', 1, type=int),
        'limit': request.args.get('limit', limit_per_page, type=int),
    }
    # Ensure limit is positive
    if filters['limit'] <= 0:
        filters['limit'] = limit_per_page
    # Ensure page is positive
    if filters['page'] <= 0:
        filters['page'] = 1

    # Remove None values so db function doesn't process them unnecessarily
    # Keep pagination params even if they are default
    active_filters = {k: v for k, v in filters.items() if v is not None and k not in ['page', 'limit']}

    try:
        # Assuming db_recipe.get_all_recipes is updated to handle pagination
        # and returns a tuple: (list_of_recipes_for_page, total_item_count)
        recipes_page, total_items = db_recipe.get_all_recipes(
            filters=active_filters,
            page=filters['page'],
            limit=filters['limit']
        )

        total_pages = (total_items + filters['limit'] - 1) // filters['limit'] # Calculate total pages

        return jsonify({
            "data": recipes_page,
            "pagination": {
                "total_items": total_items,
                "total_pages": total_pages,
                "current_page": filters['page'],
                "per_page": filters['limit']
            }
        })
    except Exception as e:
        # Log the error in a real application
        print(f"Error fetching recipes with pagination: {e}")
        abort(500, description="Internal server error fetching recipes.")


@bp.route('/<int:id>', methods=['GET'])
def get_recipe(id):
    """Get a specific recipe by its ID."""
    try:
        recipe = db_recipe.get_recipe_by_id(id)
        if recipe is None:
            abort(404, description=f"Recipe with id {id} not found.")     
        return jsonify({"data": recipe})
    except Exception as e:
        print(f"Error fetching recipe {id}: {e}")
        abort(500, description=f"Internal server error fetching recipe {id}.")


@bp.route('/random', methods=['GET'])
def get_random_recipes_route():
    """Get a specified number of random recipes."""
    count = request.args.get('count', 3, type=int)
    # Basic validation for count
    if count <= 0:
        count = 3
    count = min(count, 100)  # Limit to a maximum of 100 random recipes

    try:
        recipes = db_recipe.get_random_recipes(count)
        return jsonify({"data": recipes})
    except Exception as e:
        print(f"Error fetching random recipes: {e}")
        abort(500, description="Internal server error fetching random recipes.")


import json # Add json import at the top if not already present

# --- Image Upload Route Helper --- (Keep existing ALLOWED_EXTENSIONS and allowed_file)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# --- End Helper ---


@bp.route('/', methods=['POST'])
def create_recipe():
    """Create a new recipe from JSON data."""
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
    # Image file is handled by a separate endpoint, not here.


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

    # Image file is NOT handled here.
    # The 'image_file' key should not be expected by the model function called below.

    try:
        # Pass only the validated text data to the database function
        # Ensure db_recipe.add_recipe does NOT expect 'image_file'
        new_recipe_id = db_recipe.add_recipe(recipe_data)
        if new_recipe_id:
            # Fetch the newly created recipe (without image info initially)
            # The get_recipe_by_id -> recipe_to_dict might add image_display_url later
            # if the image is uploaded separately.
            created_recipe = db_recipe.get_recipe_by_id(new_recipe_id)
            if created_recipe:
                # Return the created recipe data (text only at this stage)
                return jsonify({
                    "message": "Recipe created successfully (text data only)",
                    "data": created_recipe # May or may not have image_display_url yet
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
        current_app.logger.error(f"Exception during recipe creation: {e}", exc_info=True) # Use logger with traceback
        # Return a more informative error message to the client
        # Avoid exposing raw exception details in production environments for security
        # Consider a generic message in production and detailed in development
        error_message = str(e) # Or a more generic message for production
        return jsonify({"message": "Internal server error creating recipe.", "error": error_message}), 500


@bp.route('/<int:id>', methods=['PUT'])
def update_recipe(id):
    """Update an existing recipe."""
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
            # Or if the data was valid but db constraints failed (less likely with validation)
            # Let's assume it means no change or non-critical issue, maybe return the existing data?
            # Or return a specific message indicating no change. For now, treat as potential issue.
            current_app.logger.warning(f"Update operation for recipe {id} reported no changes or failed.")
            # Fetch current data to see if it matches request or if there was another issue
            current_recipe = db_recipe.get_recipe_by_id(id)
            return jsonify({
                "message": "Recipe update operation completed, but may not have changed the record (data might be identical or another issue occurred).",
                "data": current_recipe # Return current state
                }), 200 # Return 200 OK but with a specific message
    except Exception as e:
        current_app.logger.error(f"Exception during recipe update for ID {id}: {e}", exc_info=True) # Use logger
        error_message = str(e) # Or generic message
        return jsonify({"message": f"Internal server error updating recipe {id}.", "error": error_message}), 500


@bp.route('/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    """Delete a recipe."""
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
            }) # Return 200 OK with confirmation
            # Alternatively, return 204 No Content:
            # return '', 204
        else:
            # If delete returns False without exception
            current_app.logger.error(f"Failed to delete recipe {id}: db_recipe.delete_recipe returned False.")
            return jsonify({"message": "Failed to delete recipe due to an unknown database issue."}), 500
    except Exception as e:
        current_app.logger.error(f"Exception during recipe deletion for ID {id}: {e}", exc_info=True) # Use logger
        error_message = str(e) # Or generic message
        return jsonify({"message": f"Internal server error deleting recipe {id}.", "error": error_message}), 500



@bp.route('/<int:id>/image', methods=['GET'])
def get_recipe_image(id):
    """Get the primary image for a recipe."""
    try:
        # Check recipe existence first
        recipe = db_recipe.get_recipe_by_id(id)
        if recipe is None:
             return jsonify({"message": f"Recipe with id {id} not found."}), 404

        image_data = db_recipe.get_recipe_primary_image_data(id)
        if image_data is None:
             # Use jsonify for consistency, even though it's a 404
             return jsonify({"message": f"No primary image found for recipe with id {id}."}), 404

        # Return the image data as a binary response
        # Assuming JPEG format, adjust if needed
        # Determine content type based on stored data if possible, or default
        # For simplicity, assuming JPEG for now. A better approach might store mime type.
        return image_data, 200, {'Content-Type': 'image/jpeg'}
    except Exception as e:
        current_app.logger.error(f"Exception fetching image for recipe {id}: {e}", exc_info=True) # Use logger
        error_message = str(e) # Or generic message
        # Cannot return JSON for image endpoint on error easily, stick to abort or simple text
        # Or return a placeholder image/error status? For now, keep abort for simplicity on binary endpoint.
        # Using abort here as returning JSON might conflict with expected binary response
        abort(500, description=f"Internal server error fetching image: {error_message}")


# --- Image Upload Route ---
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/<int:id>/image', methods=['POST'])
def upload_recipe_image(id):
    # TODO remove before commit
    print('inside post image for recipe id=' + str(id))
    """Upload an image for a specific recipe."""
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

        # Optional: Add size validation
        # max_size = 5 * 1024 * 1024 # 5MB limit
        # if len(image_data) > max_size:
        #     return jsonify({"message": f"Image file size exceeds the limit ({max_size // 1024 // 1024}MB)."}), 400

        try:
            # Call the model function to save the image data (BLOB)
            # Assuming add_recipe_image handles setting as primary or replacing existing
            # Get the database connection to manage the transaction
            db = db_recipe.get_db()
            image_id = db_recipe.add_recipe_image(id, image_data, alt_text=file.filename, is_primary=True)

            if image_id:
                 # Commit the transaction since add_recipe_image was successful
                 db.commit()
                 current_app.logger.info(f"Transaction committed for image upload (recipe {id}, image {image_id}).")
                 # Optionally, update the recipe's main image_url field if it exists and is used
                 # db_recipe.update_recipe(id, {'image_url': f'/api/recipes/{id}/image'}) # Example if using URL

                 return jsonify({
                     "message": "Image uploaded successfully",
                     "data": {"recipe_id": id, "image_id": image_id} # Return the new image ID
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
            current_app.logger.error(f"Exception saving image for recipe {id}: {e}. Transaction rolled back.", exc_info=True) # Use logger
            error_message = str(e) # Or generic message
            # Consider more specific error handling based on db operation exceptions
            return jsonify({"message": f"Internal server error saving image for recipe {id}.", "error": error_message}), 500

    else:
        # No database operation started, so no rollback needed here
        return jsonify({"message": f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}."}), 400
