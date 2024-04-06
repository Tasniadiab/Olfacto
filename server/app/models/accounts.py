from sqlalchemy import types
from app.models import db
from datetime import datetime
from flask_bcrypt import Bcrypt
from uuid import uuid4

bcrypt = Bcrypt()

def get_uuid():
    return uuid4().hex

user_category_association = db.Table(
    'user_category_association',
    db.Column('user_id', db.String(32), db.ForeignKey('users.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
)

user_brand_association = db.Table(
    'user_brand_association',
    db.Column('user_id', db.String(32), db.ForeignKey('users.id'), primary_key=True),
    db.Column('brand_id', db.Integer, db.ForeignKey('brands.id'), primary_key=True)
)

user_note_association = db.Table(
    'user_note_association',
    db.Column('user_id', db.String(32), db.ForeignKey('users.id'), primary_key=True),
    db.Column('note_id', db.Integer, db.ForeignKey('notes.id'), primary_key=True)
)

user_perfume_association = db.Table(
    'user_perfume_association',
    db.Column('user_id', db.String(32), db.ForeignKey('users.id'), primary_key=True),
    db.Column('perfume_id', db.Integer, db.ForeignKey('perfumes.id'), primary_key=True)
)

from app.models.category import Category 
from app.models.brand import Brand 
from app.models.perfume import Notes, Perfume, Comment

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    username = db.Column(db.String(100), unique=True, nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    profilepicture = db.Column(db.String(300), nullable=True)
    datejoined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category_preferences = db.relationship('Category', secondary=user_category_association,
                                           backref=db.backref('users', lazy='dynamic'))
    brand_preferences = db.relationship('Brand', secondary=user_brand_association,
                                        backref=db.backref('users', lazy='dynamic'))
    note_preferences = db.relationship('Notes', secondary=user_note_association,
                                       backref=db.backref('users', lazy='dynamic'))
    tried_perfumes = db.relationship('Perfume', secondary=user_perfume_association,
                                   backref=db.backref('users_tried', lazy='dynamic'))
    want_to_try = db.relationship('Perfume', secondary=user_perfume_association,
                                    backref=db.backref('users_want_to_try', lazy='dynamic'))
    wishlist = db.relationship('Perfume', secondary=user_perfume_association,
                                    backref=db.backref('users_wishlist', lazy='dynamic'))
    favorite_perfumes = db.relationship('Perfume', secondary=user_perfume_association,
                                    backref=db.backref('users_favorite', lazy='dynamic'))
    comments = db.relationship('Comment', backref='user_comments', cascade='all, delete-orphan')
    
    def set_password(self, pw):
        self.password = bcrypt.generate_password_hash(pw).decode('utf-8')

    # def check_password(self, pw):
    #     return bcrypt.check_password_hash(self.password, pw)




    