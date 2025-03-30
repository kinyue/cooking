# backend/tests/test_recipes_api.py
# Tests for the recipe API endpoints

import pytest
import json
from backend.app import create_app # Assuming create_app is in backend/app/__init__.py
from backend.app.models.recipe import init_db, get_db, close_db

# Fixture to create and configure a new app instance for each test
@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Use the testing configuration
    app = create_app(config_name='testing')

    # Create the database and load test data
    with app.app_context():
        init_db() # Initialize the schema
        # You might want to add some initial test data here
        # get_db().execute(...)
        # get_db().commit()

    yield app

    # Clean up / close the DB
    # This might not be strictly necessary with in-memory DB, but good practice
    with app.app_context():
        close_db()


# Fixture for the test client
@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


# --- Test Cases ---

def test_get_recipes_empty(client):
    """Test getting recipes when the database is empty."""
    response = client.get('/api/recipes')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'data' in data
    assert isinstance(data['data'], list)
    assert len(data['data']) == 0
    # assert 'pagination' in data # Add if pagination is implemented

def test_create_recipe(client, app):
    """Test creating a new recipe."""
    new_recipe_data = {
        "name": "Test Recipe",
        "description": "A recipe created for testing.",
        "ingredients": json.dumps([{"name": "Test Ingredient", "quantity": "1 unit"}]),
        "instructions": json.dumps(["Step 1: Test."]),
        "tags": json.dumps(["test", "easy"]),
        "difficulty": "简单",
        "cuisine": "测试菜",
        "prep_time_minutes": 5,
        "cook_time_minutes": 10,
        "servings": 1
    }
    response = client.post('/api/recipes',
                           data=json.dumps(new_recipe_data),
                           content_type='application/json')

    assert response.status_code == 201 # Check for Created status
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'message' in data
    assert 'data' in data
    assert data['data']['name'] == new_recipe_data['name']
    assert 'id' in data['data']
    new_recipe_id = data['data']['id']

    # Verify the recipe was actually added to the DB
    with app.app_context():
        db = get_db()
        cursor = db.execute("SELECT * FROM recipes WHERE id = ?", (new_recipe_id,))
        recipe = cursor.fetchone()
        assert recipe is not None
        assert recipe['name'] == new_recipe_data['name']

# Add more tests for GET /api/recipes (with data), GET /api/recipes/<id>,
# PUT /api/recipes/<id>, DELETE /api/recipes/<id>, error handling (404, 400) etc.

# Example test for GET /api/recipes/<id> (assuming a recipe exists)
# def test_get_specific_recipe(client, app):
#     # First, add a recipe to the DB within app_context
#     with app.app_context():
#         cursor = get_db().execute(
#             "INSERT INTO recipes (name, ingredients, instructions) VALUES (?, ?, ?)",
#             ("Existing Recipe", '[]', '[]')
#         )
#         get_db().commit()
#         recipe_id = cursor.lastrowid
#
#     response = client.get(f'/api/recipes/{recipe_id}')
#     assert response.status_code == 200
#     data = json.loads(response.data)
#     assert data['data']['id'] == recipe_id
#     assert data['data']['name'] == "Existing Recipe"
