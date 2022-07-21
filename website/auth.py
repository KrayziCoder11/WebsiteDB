from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy import true
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('sro.tdgsupport.com/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        admin = User.query.filter_by(is_admin=True).first()
        if admin:
            pass
        else:
            new_admin = User(email= "admin@gmail.com", name="admin", password=generate_password_hash("password", method='sha256'), is_active = True, is_authenticated = True, is_admin = True)
            db.session.add(new_admin)
            db.session.commit()

    if request.method == 'POST':
    
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
                
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("index.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            return render_template("sign_up_confirm.html", user=current_user, email = email, name = name, password = password1)

    return render_template("sign_up.html", user=current_user)


@auth.route('/sign_up_confirm/<check>/<email>/<name>/<password>', methods=['GET', 'POST'])
def sign_up_confirm(check, email, name, password):
    if(check == "true"):
        new_user = User(email= email, name=name, password=generate_password_hash(password, method='sha256'), is_active = True, is_authenticated = True, is_admin = False)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created!', category='success')
        return redirect(url_for('auth.login'))
    else:
        flash('Returning to Sign up page!', category='success')
        return redirect(url_for('auth.sign_up'))
        
