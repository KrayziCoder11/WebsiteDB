from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Computer, User
from . import db
from .logic import *



#defines a blueprint for the views
views = Blueprint('views', __name__)

#whenever we go to the home page (in this case, '/') the home method will run
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        c_name = request.form.get('name')
        c_num = request.form.get('serial')
        c_location = request.form.get('location')
        c_model = request.form.get('model')

        if len(c_name) < 1:
            flash('The name is too short!', category='error')
        elif len(c_location) < 1:
            flash('Invalid location!', category='error')
        elif len(c_model) < 1:
            flash('Invalid Model!', category='error')
        elif not (c_num.isdigit()):
            flash('Serial Number can only have numbers!', category='error')
        else:
            new_comp = Computer(name=c_name, serial = c_num, location = c_location, model = c_model, user_name = current_user.name)
            db.session.add(new_comp)
            db.session.commit()
            flash('Computer added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return render_template("settings.html", user = current_user)


@views.route('/edit_settings', methods=['GET', 'POST'])
@login_required
def edit_settings():
    if request.method == 'GET':
        return render_template("settings_edit.html", user = current_user)

    elif request.method == 'POST':
        user = current_user
        new_name = request.form.get('new_name')    
        new_email = request.form.get('new_email')    
        
        if(new_email != None and new_name != None ):
            user.email = new_email
            db.session.merge(user)
            db.session.flush()
            db.session.commit()
            
            user.name = new_name
            db.session.merge(user)
            db.session.flush()
            db.session.commit()
            
            return render_template("settings.html", user = current_user)


    return render_template("settings_edit.html", user = current_user)


@views.route('/admins', methods=['GET', 'POST'])
@login_required
def admins():
    all_users = User.query.filter(User.name.contains('')).all()
    admins, users = sort_admins(all_users, current_user)
    

    if request.method == 'GET':
        return render_template("admins.html", user = current_user, admins = admins, users = users, s_users = users)

    elif request.method == 'POST':
        s_name = request.form.get('search name') 
        name = request.form.get('name') 
        email = request.form.get('email') 

        s_users = User.query.filter(User.name.contains(s_name), User.name.contains(name), User.email.contains(email)).all()
        if s_users:
            filtered_users = selectionSort(s_users)
            admins, s_users = sort_admins(filtered_users, current_user)
    
            return render_template("admins.html", user = current_user, admins = admins, users = users, s_users = s_users)     


@views.route('/add_admin/<id>', methods=['GET', 'POST'])
def add_admin(id):
    user = User.query.filter_by(id = id).first()
        
    if user and not (user.is_admin):
        user.is_admin = True
        
        db.session.merge(user)
        db.session.flush()
        db.session.commit()
        
    all_users = User.query.filter(User.name.contains('')).all()
    admins, users = sort_admins(all_users, current_user)
    return render_template("admins.html", user = current_user, admins = admins, users = users, s_users = users)


@views.route('/delete_admin/<id>', methods=['GET', 'POST'])
def delete_admin(id):
    user = User.query.filter_by(id = id).first()
        
    if user and (user.is_admin):
        user.is_admin = False
        
        db.session.merge(user)
        db.session.flush()
        db.session.commit()
        
    all_users = User.query.filter(User.name.contains('')).all()
    admins, users = sort_admins(all_users, current_user)
    return render_template("admins.html", user = current_user, admins = admins, users = users, s_users = users)

