from app import create_app,db
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

load_dotenv()

app = create_app()


if __name__ == "__main__":
    app.run()