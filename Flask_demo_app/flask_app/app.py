"""Main application setup for the Flask app."""

import os

from flask import Flask

from extensions import db
from routes import app as app_routes


def create_app():
    """Create and configure the Flask application.

    Returns:
        app (Flask): The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
    db.init_app(app)
    app.register_blueprint(app_routes)

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    my_app = create_app()
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    my_app.run(debug=debug_mode)
