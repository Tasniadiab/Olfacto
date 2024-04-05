from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_migrate import Migrate
import os
from app.routes.accounts import authenticate

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
    print("Loaded configuration:")
    print(app.config)

    print("SQLALCHEMY_DATABASE_URI:", app.config['SQLALCHEMY_DATABASE_URI'])
    
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(authenticate)

    
    
    
    return app
# from app.routes import brand_routes, category_routes, perfume_routes

# # Register blueprints
# app.register_blueprint(brand_routes.bp)
# app.register_blueprint(category_routes.bp)
# app.register_blueprint(perfume_routes.bp)

