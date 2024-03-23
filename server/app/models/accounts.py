from sqlalchemy import types
from app import db 


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

    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    firstname = db.Column(db.Text, nullable=False)
    lastname = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    profilepicture = db.Column(types.LargeBinary)
    datejoined = db.Column(db.DateTime, nullable=False)
    category_preferences = db.relationship('Category', secondary=user_category_association,
                                           backref=db.backref('users', lazy='dynamic'))
    brand_preferences = db.relationship('Brand', secondary=user_brand_association,
                                        backref=db.backref('users', lazy='dynamic'))
    note_preferences = db.relationship('Note', secondary=user_note_association,
                                       backref=db.backref('users', lazy='dynamic'))
    tried_perfumes = db.relationship('Perfume', secondary=user_note_association,
                                   backref=db.backref('users_tried', lazy='dynamic'))
    want_to_try = db.relationship('Perfume', secondary=user_note_association,
                                    backref=db.backref('users_want_to_try', lazy='dynamic'))
    wishlist = db.relationship('Perfume', secondary=user_note_association,
                                    backref=db.backref('users_wishlist', lazy='dynamic'))
    favorite_perfumes = db.relationship('Perfume', secondary=user_note_association,
                                    backref=db.backref('users_favorite', lazy='dynamic'))
    




    