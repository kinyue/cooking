# backend/app/__init__.py
# Application factory and core initialization

import os
import logging # Add logging import
from flask import Flask, send_from_directory, render_template
from flask_cors import CORS

from .config import config_by_name
from .models import recipe as db_recipe # Alias to avoid naming conflict
from .routes import recipes
from .routes import daily_menus # Import the new daily_menus blueprint
from .routes import utils # Import the new utils blueprint
from .routes import secure_recipes # Import the new secure_recipes blueprint
# Import all CLI commands from the cli_commands module
from .scripts.cli_commands import init_db_command, seed_recipes_command, seed_images_command

def create_app(config_name=None):
    """Application factory function."""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'production') # Default to production for deployment

    # Define the static folder relative to the project root (where build.sh runs)
    # This assumes the backend app is run from the project root or backend/
    # Adjust path if needed based on where gunicorn runs
    static_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'dist'))

    app = Flask(__name__,
                instance_relative_config=True,
                static_folder=static_folder_path,
                static_url_path='') # Serve static files from root

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
    app.register_blueprint(utils.bp) # Register the new utils blueprint
    app.register_blueprint(secure_recipes.bp) # Register the new secure_recipes blueprint

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

    # Serve frontend static files (like JS, CSS, images)
    # This route handles requests for files within the static folder
    # Note: In production, a dedicated web server like Nginx is often more efficient
    # but this works for simple deployments on platforms like Render.
    # The static_url_path='' in Flask constructor handles most of this automatically.
    # We might need a specific route if files are nested, e.g., /assets/*
    # @app.route('/assets/<path:filename>')
    # def serve_assets(filename):
    #     return send_from_directory(os.path.join(app.static_folder, 'assets'), filename)

    # Serve the main index.html for all non-API routes (Vue Router handles client-side routing)
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_vue_app(path):
        # Check if the requested path looks like a static file first
        # This prevents the index.html from being served for actual static files
        # if they are somehow not caught by the static_url_path handler.
        if '.' in path and os.path.exists(os.path.join(app.static_folder, path)):
             return send_from_directory(app.static_folder, path)
        # Otherwise, serve the main index.html for the Vue app
        index_path = os.path.join(app.static_folder, 'index.html')
        if not os.path.exists(index_path):
            app.logger.error(f"index.html not found at {index_path}")
            return "Frontend index.html not found!", 404
        return send_from_directory(app.static_folder, 'index.html')


    return app
