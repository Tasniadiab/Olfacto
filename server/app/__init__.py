from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_session import Session
import os


load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app(environment='development'):
    app = Flask(__name__)
    
    if environment == 'development':
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DEV_DATABASE_URL")
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
        
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config.from_object('config.Config')
    print("Loaded configuration:")
    print(app.config)

    Session(app)

    print("SQLALCHEMY_DATABASE_URI:", app.config['SQLALCHEMY_DATABASE_URI'])
    from app.models.accounts import User, user_perfume_association, user_brand_association, user_category_association, user_note_association
    from app.models.perfume import Notes,Perfume, perfume_category
    from app.models.category import Category
    from app.models.brand import Brand
    db.init_app(app)
    migrate.init_app(app, db)

  
    

    from app.routes.accounts import authenticate
    app.register_blueprint(authenticate)

    
    @app.route('/')
    def hello_world():
        return("hello yo")
    
    return app


# from app.routes import brand_routes, category_routes, perfume_routes

# # Register blueprints
# app.register_blueprint(brand_routes.bp)
# app.register_blueprint(category_routes.bp)
# app.register_blueprint(perfume_routes.bp)

