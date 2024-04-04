from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from models.accounts import User
from app import create_app,db


app = create_app()

bcrypt = Bcrypt(app)
@app.route("/register", methods=["POST"])
def register_user():
    email = request.json["email"]
    username = request.json["username"]
    firstname = request.json["firstname"]
    lastname = request.json["lastname"]
    password = request.json["password"]

    existing_email = User.query.filter_by(email=email).first() is not None
    existing_username = User.query.filter_by(username=username).first() is not None

    if existing_email:
        return jsonify({"error": "email already exists"})
    
    if existing_username:
        return jsonify({"error": "username already exists"})

    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(email=email, username=username, firstname=firstname, lastname=lastname, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "id": new_user.id,
        "email": new_user.email,
        "firstname": new_user.firstname,
        "lastname": new_user.lastname,
        "username": new_user.username
    })


    
    