# backend/app/routes/recipes.py
# Routes for recipe related operations
from flask import Blueprint, jsonify, request, abort
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
        'tags': request.args.get('tags'), # Needs parsing if multiple tags
        'difficulty': request.args.get('difficulty'),
        'cuisine': request.args.get('cuisine'),
        'sort': request.args.get('sort'),
        'order': request.args.get('order'),
        # Add pagination params:
        'page': request.args.get('page', 1, type=int),
        'limit': request.args.get('limit', limit_per_page, type=int), # Default limit to 8 per page
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


@bp.route('/', methods=['POST'])
def create_recipe():
    """Create a new recipe."""
    data = request.get_json()
    if not data or not data.get('name') or not data.get('ingredients') or not data.get('instructions'):
         abort(400, description="Missing required fields: name, ingredients, instructions.")

    # Basic validation could be added here

    try:
        new_recipe_id = db_recipe.add_recipe(data)
        if new_recipe_id:
            created_recipe = db_recipe.get_recipe_by_id(new_recipe_id) # Fetch the created recipe to return it
            return jsonify({
                "message": "Recipe created successfully",
                "data": created_recipe
            }), 201 # HTTP status code for Created
        else:
             abort(500, description="Failed to create recipe.")
    except Exception as e:
        print(f"Error creating recipe: {e}")
        abort(500, description="Internal server error creating recipe.")


@bp.route('/<int:id>', methods=['PUT'])
def update_recipe(id):
    """Update an existing recipe."""
    data = request.get_json()
    print(f"Received data for update: {data}")
    if not data:
        abort(400, description="No data provided for update.")

    # Check if recipe exists before attempting update
    existing_recipe = db_recipe.get_recipe_by_id(id)
    if existing_recipe is None:
        abort(404, description=f"Recipe with id {id} not found.")

    try:
        success = db_recipe.update_recipe(id, data)
        if success:
            updated_recipe = db_recipe.get_recipe_by_id(id) # Fetch updated data
            return jsonify({
                "message": "Recipe updated successfully",
                "data": updated_recipe
            })
        else:
            # This might happen if the update query affects 0 rows unexpectedly
             abort(500, description="Failed to update recipe.")
    except Exception as e:
        print(f"Error updating recipe {id}: {e}")
        abort(500, description=f"Internal server error updating recipe {id}.")


@bp.route('/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    """Delete a recipe."""
    # Check if recipe exists before attempting delete
    existing_recipe = db_recipe.get_recipe_by_id(id)
    if existing_recipe is None:
        abort(404, description=f"Recipe with id {id} not found.")

    try:
        success = db_recipe.delete_recipe(id)
        if success:
            return jsonify({
                "message": "Recipe deleted successfully",
                "data": {"id": id}
            })
            # Alternatively, return 204 No Content:
            # return '', 204
        else:
            abort(500, description="Failed to delete recipe.")
    except Exception as e:
        print(f"Error deleting recipe {id}: {e}")
        abort(500, description=f"Internal server error deleting recipe {id}.")



@bp.route('/<int:id>/image', methods=['GET'])
def get_recipe_image(id):
    """Get the primary image for a recipe."""
    try:
        image_data = db_recipe.get_recipe_primary_image_data(id)
        if image_data is None:
            abort(404, description=f"No primary image found for recipe with id {id}.")
        
        # Return the image data as a binary response
        # Assuming JPEG format, adjust if needed
        return image_data, 200, {'Content-Type': 'image/jpeg'} 
    except Exception as e:
        print(f"Error fetching image for recipe {id}: {e}")
        abort(500, description=f"Internal server error fetching image for recipe {id}.")
