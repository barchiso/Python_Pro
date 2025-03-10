"""Handles routes for user registration, login, dashboard, and logout."""
from flask import Blueprint, flash, redirect, render_template, session, url_for
from werkzeug.security import generate_password_hash

from auth import authenticate, login_required
from extensions import db
from forms import LoginForm, RegistrationForm
from models import User

app = Blueprint('app', __name__)


@app.route('/')
def home():
    """Render the homepage with links to login and register.

    Returns:
        Response: The rendered homepage template.
    """
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration by validating and creating a new user.

    Returns:
        Response: Redirects to login if successful
            or renders registration form.
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.',
                  'danger')
            return redirect(url_for('app.register'))

        # Create and store the new user
        user = User(username=username,
                    password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered!', 'success')
        return redirect(url_for('app.login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login by authenticating the provided credentials.

    Returns:
        Response: Redirects to dashboard if login is successful
            or renders login form.
    """
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = authenticate(username, password)
        if user:
            session['user_id'] = user.id
            flash('You have successfully logged in!', 'success')
            return redirect(url_for('app.dashboard'))
        flash('Invalid username or password!', 'danger')
    return render_template('login.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    """Render the user dashboard after login.

    Returns:
        Response: The rendered dashboard template with username.
    """
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', username=user.username)


@app.route('/logout')
def logout():
    """Log the user out and redirect to homepage.

    Returns:
        Response: Redirects to homepage after logging out.
    """
    session.pop('user_id', None)
    flash('You have successfully logged out!', 'info')
    return redirect(url_for('app.home'))


@app.route('/users')
def users():
    """Display the total number of registered users.

    Returns:
        Response: The rendered users template showing
            the total number of users.
    """
    total_users = User.query.count()
    return render_template('users.html', total_users=total_users)
