# backend/app/__init__.py
# Application factory and core initialization

import os
from flask import Flask
from flask_cors import CORS

from .config import config_by_name
from .models import recipe as db_recipe # Alias to avoid naming conflict
from .routes import recipes

def create_app(config_name=None):
    """Application factory function."""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')

    app = Flask(__name__, instance_relative_config=True)

    # Load configuration
    app.config.from_object(config_by_name[config_name])
    # Load the instance config, if it exists, when not testing
    # This allows overriding settings in instance/config.py
    if not app.config['TESTING']:
        app.config.from_pyfile('config.py', silent=True)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass # Already exists

    # Initialize extensions
    CORS(app, resources={r"/api/*": {"origins": "*"}}) # Allow all origins for API routes for now

    # Initialize database functions
    db_recipe.init_app(app)

    # Register blueprints
    app.register_blueprint(recipes.bp)

    # Add a simple route for health check or root
    @app.route('/hello')
    def hello():
        return 'Hello, World from Backend!'

    return app
