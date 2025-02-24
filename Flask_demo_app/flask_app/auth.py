"""SAuthentication and session management utilities for the Flask app."""
from functools import wraps

from flask import flash, redirect, session, url_for
from werkzeug.security import check_password_hash

from models import User


def authenticate(username, password):
    """Authenticate a user by verifying the username and password.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        User: The authenticated user object if valid, otherwise None.
    """
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return user
    return None


def login_required(f):
    """Ensure the user is authenticated before accessing the route.

    Args:
        f (function): The view function to be wrapped.

    Returns:
        function: The wrapped view function with authentication check.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None:
            flash('You need to login first!', 'warning')
            return redirect(url_for('app.login'))
        return f(*args, **kwargs)
    return decorated_function
