from app import create_app, db

app = create_app()

with app.app_context():
    # Perform database operations
    db.create_all()


