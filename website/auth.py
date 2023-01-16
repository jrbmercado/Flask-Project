from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)  # Setup blueprint


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Filter all users that have this email from the database
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                # After restarting webserver this will be cleared, or customer clears history, otherwise it will remember you logged in previously
                login_user(user, remember=True)
                # Redirect to the homepage after successful login
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password, try again", category="error")
        else:
            flash("Email does not exist", category="error")

    return render_template("login.html", user=current_user)

# We dont want to be able to use this function unless logged in


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    # Redirect to login page
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # Get all info from the form
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email already exists", category="error")
        # Check inputs
        elif len(email) < 4:
            flash("Email must be greater than 3 characters", category="error")
        elif len(first_name) < 2:
            flash("Name must be greater than 1 character", category="error")
        elif password1 != password2:
            flash("Passwords don\'t match", category="error")
        elif len(password1) < 7:
            flash("Password must be at least 7 characters", category="error")
        else:
            # Add user to database with password hashing
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)  # Add new user to database
            db.session.commit()  # Commit changes to database
            flash("Account created", category="success")
            # Find the url that is mapped to the location for home (blueprint name . function name)
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
