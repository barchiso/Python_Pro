"""Model for the User entity in the Flask app."""

from extensions import db


class User(db.Model):
    """Represents a user in the database.

    Attributes:
        id (int): The unique identifier for the user (primary key).
        username (str): The unique username of the user (must be unique).
        password (str): The hashed password of the user.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
