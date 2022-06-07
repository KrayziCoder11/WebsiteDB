from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Computer
from . import db
import json



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

        if len(c_name) < 1:
            flash('The name is too short!', category='error')
        elif len(c_location) < 1:
            flash('Invalid location!', category='error')
        elif not (c_num.isdigit()):
            flash('Serial Number can only have numbers!', category='error')
        else:
            new_comp = Computer(name=c_name, serial = c_num, location = c_location)
            db.session.add(new_comp)
            db.session.commit()
            print(c_num)
            flash('Computer added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-computer/<serial>/<name>', methods=['GET', 'POST'])
def delete_computer(serial, name):
    computer = Computer.query.filter_by(serial = serial).first()
        
    if computer:
        db.session.delete(computer)
        db.session.commit()
    
    
    computers = Computer.query.filter(Computer.name.contains(name)).all()
    if len(computers) < 1:
        flash('There are no more computers in the database, please add more', category='success')
        return render_template("home.html", user=current_user)
    else:
        return render_template("search.html", user = current_user, computers = computers, name = name)


@views.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        name = request.form.get('name') 
               
        computers = Computer.query.filter(Computer.name.contains(name)).all()
        if computers:
            return render_template("search.html", user = current_user, computers = computers, name = name)
                
    return render_template("search.html", user = current_user)


@views.route('/edit/<serial>', methods=['GET', 'POST'])
@login_required
def edit(serial):
    if request.method == 'POST':
        computer = Computer.query.filter_by(serial = serial).first()
        new_name = request.form.get('new_name')    
        new_serial = request.form.get('new_serial')    
        new_location = request.form.get('new_location')          
        
        if computer:
            if(new_location != None and new_name != None and new_location != None):
                computer.location = new_location
                db.session.merge(computer)
                db.session.flush()
                db.session.commit()
                
                computer.name = new_name
                db.session.merge(computer)
                db.session.flush()
                db.session.commit()
                
                computer.serial = new_serial
                db.session.merge(computer)
                db.session.flush()
                db.session.commit()
                
                return render_template("search.html", user = current_user)


    return render_template("edit.html", user = current_user)

