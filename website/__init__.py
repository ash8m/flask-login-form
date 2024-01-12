from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy_utils import database_exists, create_database

db=SQLAlchemy()
DB_NAME = "users.db"

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "adsfjwuenvcjWEOPoiajfjsndsiuhwe"
    app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql://root:password@app-sql-db-1:3306/{DB_NAME}'
    db.init_app(app)
    if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
        create_database(app.config["SQLALCHEMY_DATABASE_URI"])
        print('Created Database!')


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
