from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Computer, User
from . import db
from .logic import *
from website import logic

SEARCH_PARAM = []

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


@views.route('/delete-computer/<serial>', methods=['GET', 'POST'])
def delete_computer(serial):
    computer = Computer.query.filter_by(serial = serial).first()
        
    if computer:
        db.session.delete(computer)
        db.session.commit()
    
    computers = Computer.query.filter(Computer.name.contains("")).all()
    if len(computers) < 1:
        flash('There are no more computers in the database, please add more', category='success')
        return render_template("home.html", user=current_user)
    else:
        models = get_models(computers)
        users = get_user_names(computers)
        locations = get_locations(computers) 
        table_computers = get_ten(computers, 1) 
        max = get_max_pages(computers)      
        return render_template("search.html", user = current_user, computers = computers, models = models, users = users, locations = locations, table_computers = table_computers, page = 1, max = max)


@views.route('/delete_confirm/<serial>', methods=['GET', 'POST'])
def delete_confirm(serial):
    if request.method == 'GET':
        computer = Computer.query.filter_by(serial = serial).first()
        return render_template("delete_confirmation.html", user = current_user, c = computer)


@views.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    computers = Computer.query.filter(Computer.name.contains('')).all()
    computers = selectionSort(computers)
    models = get_models(computers)
    users = get_user_names(computers)
    locations = get_locations(computers)
    max = get_max_pages(computers)      
        
    if len(computers) == 0:
        table_computers = []
        max = 1
    else:  
        table_computers = get_ten(computers, 1)
    
            
            
    if request.method == 'GET':
        if computers:
            SEARCH_PARAM.clear()
            return render_template("search.html", user = current_user, computers = computers, models = models, users = users, locations = locations, table_computers = table_computers, page = 1, max = max)
    elif request.method == 'POST':
        c_name = request.form.get('name') 
        c_model = request.form.get('model') 
        c_location = request.form.get('location') 
        c_user = request.form.get('user') 
        c_is_active = request.form.get('active') 
        SEARCH_PARAM.clear()
        SEARCH_PARAM.append(c_name)
        SEARCH_PARAM.append(c_model)
        SEARCH_PARAM.append(c_location)
        SEARCH_PARAM.append(c_user)
        SEARCH_PARAM.append(c_is_active)
              
        computers = Computer.query.filter(Computer.name.contains(c_name), Computer.model.contains(c_model), Computer.location.contains(c_location), Computer.user_name.contains(c_user), Computer.is_active.contains(c_is_active)).all()
        if computers:
            computers = selectionSort(computers)
            models = get_models(computers)
            users = get_user_names(computers)
            locations = get_locations(computers)
            table_computers = get_ten(computers, 1)
            max = get_max_pages(computers)      
        
            return render_template("search.html", user = current_user, computers = computers, models = models, users = users, locations = locations, table_computers = table_computers, page = 1, max = max)
    return render_template("search.html", user = current_user, computers = computers, models = models, users = users, locations = locations, table_computers = table_computers, page = 1, max = max)


@views.route('/turn/<page>', methods=['GET', 'POST'])
@login_required
def turn(page):
    page = int(page)
    if page < 1:
        page = 1
    if len(SEARCH_PARAM) == 5:
        computers = Computer.query.filter(Computer.name.contains(SEARCH_PARAM[0]), Computer.model.contains(SEARCH_PARAM[1]), Computer.location.contains(SEARCH_PARAM[2]), Computer.user_name.contains(SEARCH_PARAM[3]), Computer.is_active.contains(SEARCH_PARAM[4])).all()
    else:
        computers = Computer.query.filter(Computer.name.contains('')).all()
        

    models = get_models(computers) 
    users = get_user_names(computers)
    locations = get_locations(computers)
    max = get_max_pages(computers)      
        
    if (len(computers) % 10 == 0):
        num_pages = len(computers) / 10 
        if page > num_pages:
            page = int(num_pages)
        
    else:
        num_pages = float(len(computers)) / 10 
        if page > int(num_pages) + 1:
            page = int(num_pages) + 1
        
    if len(computers) == 0:
        table_computers = []
        max = 1
    else:
        table_computers = get_ten(computers, page)
    
            
    return render_template("search.html", user = current_user, computers = computers, models = models, users = users, locations = locations, table_computers = table_computers, page = page, max = max)


@views.route('/computer_edit/<serial>', methods=['GET', 'POST'])
@login_required
def computer_edit(serial):
    
    if request.method == 'GET':
        return render_template("computer_edit.html", user = current_user)
    elif request.method == 'POST':
        computer = Computer.query.filter_by(serial = serial).first()
        new_name = request.form.get('new_name')    
        new_serial = request.form.get('new_serial')    
        new_location = request.form.get('new_location')
        new_model = request.form.get('model')          
        new_user = request.form.get('new_user')
        new_active = request.form.get('active')
        
        if computer:
            if len(new_name) < 1:
                flash('The computer name is too short!', category='error')
            elif len(new_user) < 1:
                flash('The user name is too short!', category='error')
            elif len(new_location) < 1:
                flash('Invalid location!', category='error')
            elif len(new_model) < 1:
                flash('Invalid Model!', category='error')
            elif not (new_serial.isdigit()):
                flash('Serial Number can only have numbers!', category='error')
            elif new_active == None:
                flash("Select whether the computer is active", category = "error")
        
            elif(new_active != None and new_model != None and new_user != None and new_location != None and new_name != None and new_location != None):
                computer.location = new_location
                computer.is_active = new_active
                computer.name = new_name
                computer.model = new_model
                computer.serial = new_serial
                computer.user_name = new_user
                
                
                db.session.merge(computer)
                db.session.flush()
                db.session.commit()
                
                computers = Computer.query.filter(Computer.name.contains('')).all()
                models = get_models(computers)
                users = get_user_names(computers)
                locations = get_locations(computers)
                table_computers = get_ten(computers, 1)
                max = get_max_pages(computers)      
        
                return render_template("search.html", user = current_user, computers = computers, models = models, users = users, locations = locations, table_computers = table_computers, page = 1, max = max)
    return render_template("home.html", user = current_user)


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

