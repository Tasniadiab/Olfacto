from flask import Flask, Blueprint, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_session import Session
from app.models.accounts import User
from app.models import db

app = Flask(__name__)

authenticate = Blueprint('authenticate', __name__)

bcrypt = Bcrypt(app)

@authenticate.route("/@me")
def get_current_user():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "no account under this email"}), 401
    
    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        "id": user.id,
        "email": user.email,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "username": user.username
    })


@authenticate.route("/register", methods=["POST"])
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
        return jsonify({"error": "username already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(email=email, username=username, firstname=firstname, lastname=lastname, password=hashed_password)
    new_user.set_password(password) 
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "id": new_user.id,
        "email": new_user.email,
        "firstname": new_user.firstname,
        "lastname": new_user.lastname,
        "username": new_user.username
    })

@authenticate.route("/login", methods=["POST"])
def login_user():
    email = request.json["email"]
    password = request.json["password"]

    user = User.query.filter_by(email=email).first()

    if user is None: 
        return jsonify({"error": "no account under this email"}), 401
    
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "password is incorrect"}), 401
    
    session["user_id"] = user.id
    
    return jsonify({
        "id": user.id,
        "email": user.email,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "username": user.username
    })


@authenticate.route('/signout', methods=['GET'])
def sign_out():
    session.pop('user_id', None) 

    return jsonify({
        "msg": "You have been successfully signed out."
    })
   