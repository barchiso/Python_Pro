"""Forms for user registration and login in the Flask app."""

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length


class RegistrationForm(FlaskForm):
    """Form for user registration.

    Args:
        username (StringField): The username field.
        password (PasswordField): The password field.
        confirm_password (PasswordField): The field to confirm the password.
        submit (SubmitField): The submit button for the form.
    """

    username = StringField('Username', validators=[
        DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    """Form for user login with username and password.

    Args:
        username (StringField): The username field.
        password (PasswordField): The password field.
        submit (SubmitField): The submit button for the form.
    """

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
