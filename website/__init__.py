from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'The access code is... access code'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User
    #recreate_database(app)
    create_new_database(app)
    

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
    


def recreate_database(app):
    if not path.exists('website/' + DB_NAME):
        db.drop_all(app=app)
        db.create_all(app=app)

        print('Created Database!')

def create_new_database(app):
    db.drop_all(app=app)
    db.create_all(app=app)

    print('Created Database!')
