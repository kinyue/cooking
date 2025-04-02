# backend/app/routes/recipes.py
# Routes for recipe related operations
from flask import Blueprint, jsonify, request, abort
from ..models import recipe as db_recipe # Import database functions

bp = Blueprint('recipes', __name__, url_prefix='/api/recipes')

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
        # Add pagination params if needed:
        # 'page': request.args.get('page', 1, type=int),
        # 'limit': request.args.get('limit', 10, type=int),
    }
    # Remove None values so db function doesn't process them unnecessarily
    filters = {k: v for k, v in filters.items() if v is not None}

    try:
        recipes = db_recipe.get_all_recipes(filters=filters)
        # Basic pagination structure (if implemented in db_recipe)
        # return jsonify({
        #     "data": recipes,
        #     "pagination": { ... }
        # })
        return jsonify({"data": recipes})
    except Exception as e:
        # Log the error in a real application
        print(f"Error fetching recipes: {e}")
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
