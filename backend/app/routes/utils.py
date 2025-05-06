# backend/app/routes/utils.py
# Utility routes

from flask import Blueprint, current_app, send_file, abort
import os

bp = Blueprint('utils', __name__, url_prefix='/api')

@bp.route('/download-database', methods=['GET'])
def download_database():
    """
    Download the database.db file.
    """
    try:
        # Construct the path to the database file relative to the current file's location
        # This assumes the instance folder is at backend/instance relative to the project root
        database_path = os.path.join(os.path.dirname(__file__), '..', '..', 'instance', 'database.db')
        return send_file(database_path, as_attachment=True)
    except Exception as e:
        current_app.logger.error(f"Error downloading database: {e}", exc_info=True)
        abort(500, description="Internal server error downloading database.")
