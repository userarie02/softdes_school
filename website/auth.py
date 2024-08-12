from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from flask_migrate import Migrate



auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print(f"Authenticated User: {current_user.email}, Role: {current_user.role}")  # Debugging line
        if current_user.role == 'admin':
            return redirect(url_for('views.admin_dashboard'))
        elif current_user.role == 'teacher':
            return redirect(url_for('views.teacher_dashboard'))
        elif current_user.role == 'student':
            return redirect(url_for('views.student_dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            flash('Logged in successfully!', category='success')
            login_user(user, remember=True)
            
            if user.role == 'admin':
                return redirect(url_for('views.admin_dashboard'))
            elif user.role == 'teacher':
                return redirect(url_for('views.teacher_dashboard'))
            elif user.role == 'student':
                return redirect(url_for('views.student_dashboard'))
        else:
            flash('Invalid credentials, please try again.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout',  methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', category='success')
    return redirect(url_for('auth.login'))

@auth.route('/sign-up',  methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        role = request.form.get('role')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')


        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif password1 != password2:
            flash('Password don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, password=generate_password_hash(password1, method='pbkdf2:sha256'), role=role)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('auth.login'))
        

    return render_template("sign_up.html", user=current_user)

