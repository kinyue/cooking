# backend/app/__init__.py
# Application factory and core initialization

import os
import logging # Add logging import
from flask import Flask
from flask_cors import CORS

from .config import config_by_name
from .models import recipe as db_recipe # Alias to avoid naming conflict
from .routes import recipes
from .routes import daily_menus # Import the new daily_menus blueprint
# Import all CLI commands from the cli_commands module
from .scripts.cli_commands import init_db_command, seed_recipes_command, seed_images_command

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
    app.register_blueprint(daily_menus.bp)

    # Register CLI commands
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_recipes_command)
    app.cli.add_command(seed_images_command)

    # Add debug log before publish
    app.logger.setLevel(logging.DEBUG)

    # Add a simple route for health check or root
    @app.route('/hello')
    def hello():
        return 'Hello, World from Backend!'

    return app
