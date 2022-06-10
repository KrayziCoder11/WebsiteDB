from . import db
from sqlalchemy.sql import func
class Computer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    serial = db.Column(db.Integer)
    location = db.Column(db.String(150))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    is_active = db.Column(db.Boolean)
    is_authenticated = db.Column(db.Boolean)
    is_admin = db.Column(db.Boolean)
    