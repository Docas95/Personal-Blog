# this file takes care of all the backend stuff related to signin up/logging in/logging ou users
from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.utils import redirect
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        # get the username and password inserted by the user
        username = request.form.get('username')
        password = request.form.get('password')

        # check if that username exists
        user = User.query.filter_by(username=username).first()

        if user:
            # check if the password given matches the password of the user
            if check_password_hash(user.password, password):
                login_user(user, remember='True')
                flash('Logged in successfully.', category="success")
                return redirect(url_for('views.archive'))
            else:
                flash('Incorrect password.', category='error')
        else:
            flash('This user does not exist.', category='error')

    return render_template('login.html', user=current_user)

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        # get the info from the form submitted by the user
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # check if the username and email already exist in the database
        user_email = User.query.filter_by(email=email).first()
        user_username = User.query.filter_by(username=username).first()

        if user_email:
            flash('Email already exists.', category='error')
        elif user_username:
            flash('Username already exists.', category='error')
        elif len(email) < 5:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(username) < 2:
            flash('Username must be creater than 1 character.', category='error')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters long.', category='error')
        elif len(password1) > 20:
            flash('Password can\'t be greater than 20 characters long', category='error')
        elif password1 != password2:
            flash('The two passwords don\'t match', category='error')
        else:
            # add user to the database 
            new_user = User(username=username, email=email, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully!', category='success')
            return redirect(url_for('auth.login'))

    return render_template('sign_up.html', user=current_user)

@auth.route('/logout')
@login_required
def lougout():
    logout_user()
    return redirect(url_for('auth.login'))