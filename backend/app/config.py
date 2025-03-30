# backend/app/config.py
# Basic Flask application configuration

import os

# Determine the base directory of the application
# This helps in constructing absolute paths, especially for the database file
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) # This should point to the 'backend' directory

class Config:
    """Base configuration class."""
    # Secret key for signing session cookies and other security related needs
    # IMPORTANT: Keep this secret in production! Load from env var or instance config.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-should-really-change-this'

    # Database configuration
    # Default to a file named 'database.db' inside the 'backend' folder for testing path issues
    # The 'instance' folder is typically outside the 'app' package and not version controlled
    DATABASE = os.environ.get('DATABASE_URL') or \
        os.path.join(basedir, 'instance', 'database.db')

    # Disable SQLAlchemy event system if not using SQLAlchemy, saves resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Relevant if using Flask-SQLAlchemy

    # Other potential configurations
    DEBUG = False # Set to True for development debugging (use FLASK_ENV=development instead)
    TESTING = False

class DevelopmentConfig(Config):
    """Development specific configuration."""
    DEBUG = True
    # In development, maybe use a different DB or specific settings
    # DATABASE = os.path.join(basedir, 'instance', 'dev_database.db')

class TestingConfig(Config):
    """Testing specific configuration."""
    TESTING = True
    # Use an in-memory SQLite database for tests
    DATABASE = 'sqlite:///:memory:' # In-memory SQLite DB for testing
    # Or use a file:
    # DATABASE = os.path.join(basedir, 'instance', 'test_database.db')
    SECRET_KEY = 'test-secret-key' # Use a fixed key for tests

class ProductionConfig(Config):
    """Production specific configuration."""
    # Ensure SECRET_KEY is set via environment variable in production
    # Ensure DEBUG and TESTING are False (default)
    pass

# Dictionary to easily access configuration classes by name
config_by_name = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig,
    default=DevelopmentConfig # Default to development if FLASK_ENV is not set
)

def get_config_by_name(config_name):
    """Helper function to get config class by name."""
    return config_by_name.get(config_name, DevelopmentConfig)
