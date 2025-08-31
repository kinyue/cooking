#!/usr/bin/env python3
"""
WSGI entry point for gunicorn
"""

import os
import sys

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set the Flask app environment variable
os.environ.setdefault('FLASK_ENV', 'production')

# Import and create the app
from app import create_app

# Create the application instance
app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)