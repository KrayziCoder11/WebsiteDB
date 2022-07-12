from xmlrpc.client import Boolean
from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Computer
from . import db
from .logic import *


SEARCH_PARAM = []
search_page = Blueprint('search_page', __name__)


@search_page.route('/delete-computer/<serial>', methods=['GET', 'POST'])
def delete_computer(serial):
    computer = Computer.query.filter_by(serial = serial).first()
        
    if computer:
        db.session.delete(computer)
        db.session.commit()
    
    computers = Computer.query.filter(Computer.name.contains("")).all()
    computers = selectionSort(computers)
    
    
    if len(computers) < 1:
        flash('There are no more computers in the database, please add more', category='success')
        return render_template("home.html", user=current_user)
    else:
        models = get_models(computers)
        users = get_user_names(computers)
        locations = get_locations(computers) 
        if len(SEARCH_PARAM) == 5:
            computers = Computer.query.filter(Computer.name.contains(SEARCH_PARAM[0]), Computer.model.contains(SEARCH_PARAM[1]), Computer.location.contains(SEARCH_PARAM[2]), Computer.user_name.contains(SEARCH_PARAM[3]), Computer.is_active.contains(SEARCH_PARAM[4])).all()
            computers = selectionSort(computers)
    
        max = get_max_pages(computers)  
        table_computers = get_ten(computers, 1) 
        max_array = []
        for i in range(1, max + 1):
            max_array.append(i)
        return render_template("search.html", user = current_user, filtered = False, models = models, users = users, locations = locations, table_computers = table_computers, page = 1, max = max, max_array = max_array, filter = SEARCH_PARAM)


@search_page.route('/delete_confirm/<serial>', methods=['GET', 'POST'])
def delete_confirm(serial):
    if request.method == 'GET':
        computer = Computer.query.filter_by(serial = serial).first()
        return render_template("delete_confirmation.html", user = current_user, c = computer)


@search_page.route('/search', methods=['GET', 'POST'])
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
    max_array = []
    for i in range(1, max + 1):
        max_array.append(i)
                
            
    if request.method == 'GET':
        SEARCH_PARAM.clear()
        if computers:
            return render_template("search.html", user = current_user, filtered = False, filter = SEARCH_PARAM, models = models, users = users, max_array = max_array, locations = locations, table_computers = table_computers, page = 1, max = max)
        elif len(computers) == 0:
            return render_template("search.html", user = current_user, filtered = False, filter = SEARCH_PARAM, models = models, users = users, max_array = max_array, locations = locations, table_computers = table_computers, page = 1, max = max)
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
        if computers and len(computers) > 0:
            computers = selectionSort(computers)
            models = get_models(computers)
            users = get_user_names(computers)
            locations = get_locations(computers)
            table_computers = get_ten(computers, 1)
            max = get_max_pages(computers)    
            max_array = []
            for i in range(1, max + 1):
                max_array.append(i)  
                
            return render_template("search.html", user = current_user, filtered = (len(SEARCH_PARAM) > 0), filter = SEARCH_PARAM, models = models, users = users, locations = locations, table_computers = table_computers, page = 1, max = max, max_array = max_array)
        else:
            return render_template("search.html", user = current_user, filtered = (len(SEARCH_PARAM) > 0), models = [], filter = SEARCH_PARAM, users = [], locations = [], table_computers = [], page = 1, max = 1, max_array = max_array)


@search_page.route('/turn/<page>', methods=['GET', 'POST'])
@login_required
def turn(page):
    if request.method == 'GET':
        page = int(page)
        if page < 1:
            page = 1
        
        if len(SEARCH_PARAM) == 5:
            computers = Computer.query.filter(Computer.name.contains(SEARCH_PARAM[0]), Computer.model.contains(SEARCH_PARAM[1]), Computer.location.contains(SEARCH_PARAM[2]), Computer.user_name.contains(SEARCH_PARAM[3]), Computer.is_active.contains(SEARCH_PARAM[4])).all()
        
        else:
            computers = Computer.query.filter(Computer.name.contains('')).all()
        computers = selectionSort(computers)
        

        models = get_models(computers) 
        users = get_user_names(computers)
        locations = get_locations(computers)
        max = get_max_pages(computers) 
        max_array = []
        for i in range(1, max + 1):
            max_array.append(i)

            
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
        
        return render_template("search.html", user = current_user, filtered = (len(SEARCH_PARAM) > 0), models = models, filter = SEARCH_PARAM, users = users, locations = locations, table_computers = table_computers, page = page, max = max, max_array = max_array)
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
            max_array = []
            for i in range(1, max + 1):
                max_array.append(i)  
                
            return render_template("search.html", filtered = (len(SEARCH_PARAM) > 0), user = current_user, models = models, filter = SEARCH_PARAM, users = users, locations = locations, table_computers = table_computers, page = page, max = max, max_array = max_array)


@search_page.route('/computer_edit/<serial>', methods=['GET', 'POST'])
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
                
                if len(SEARCH_PARAM) == 5:
                    computers = Computer.query.filter(Computer.name.contains(SEARCH_PARAM[0]), Computer.model.contains(SEARCH_PARAM[1]), Computer.location.contains(SEARCH_PARAM[2]), Computer.user_name.contains(SEARCH_PARAM[3]), Computer.is_active.contains(SEARCH_PARAM[4])).all()
                computers = selectionSort(computers)
    
                models = get_models(computers)
                users = get_user_names(computers)
                locations = get_locations(computers)
                table_computers = get_ten(computers, 1)
                max = get_max_pages(computers)  
                
                max_array = []
                for i in range(1, max + 1):
                    max_array.append(i)  
        
                return render_template("search.html", filtered = False, user = current_user, filter = SEARCH_PARAM, models = models, users = users, locations = locations, table_computers = table_computers, page = 1, max = max, max_array = max_array)
    return render_template("home.html", user = current_user)


