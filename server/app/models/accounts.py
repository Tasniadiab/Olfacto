from sqlalchemy import types
from app import db 
from uuid import uuid4


def get_uuid():
    return uuid4().hex

user_category_association = db.Table(
    'user_category_association',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
)

user_brand_association = db.Table(
    'user_brand_association',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('brand_id', db.Integer, db.ForeignKey('brands.id'), primary_key=True)
)

user_note_association = db.Table(
    'user_note_association',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('note_id', db.Integer, db.ForeignKey('notes.id'), primary_key=True)
)

user_perfume_association = db.Table(
    'user_perfume_association',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('perfume_id', db.Integer, db.ForeignKey('perfumes.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    username = db.Column(db.String(100), unique=True, nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    profilepicture = db.Column(types.LargeBinary, nullable=True)
    datejoined = db.Column(db.DateTime, nullable=False)
    category_preferences = db.relationship('Category', secondary=user_category_association,
                                           backref=db.backref('users', lazy='dynamic'),nullable=True)
    brand_preferences = db.relationship('Brand', secondary=user_brand_association,
                                        backref=db.backref('users', lazy='dynamic'),nullable=True)
    note_preferences = db.relationship('Note', secondary=user_note_association,
                                       backref=db.backref('users', lazy='dynamic'),nullable=True)
    tried_perfumes = db.relationship('Perfume', secondary=user_note_association,
                                   backref=db.backref('users_tried', lazy='dynamic'),nullable=True)
    want_to_try = db.relationship('Perfume', secondary=user_note_association,
                                    backref=db.backref('users_want_to_try', lazy='dynamic'),nullable=True)
    wishlist = db.relationship('Perfume', secondary=user_note_association,
                                    backref=db.backref('users_wishlist', lazy='dynamic'),nullable=True)
    favorite_perfumes = db.relationship('Perfume', secondary=user_note_association,
                                    backref=db.backref('users_favorite', lazy='dynamic'),nullable=True)
    




    