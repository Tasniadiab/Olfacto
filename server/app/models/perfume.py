from app import db


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    perfume_id = db.Column(db.Integer, db.ForeignKey('perfumes.id'))

    user = db.relationship('User', back_populates='comments', cascade='all, delete-orphan')
    perfume = db.relationship('Perfume', backref='comments', lazy='dynamic')

class Notes(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    note = db.Column(db.Text, unique=True, nullable=False)

perfume_note_association = db.Table(
    'perfume_note',
    db.Column('perfume_id', db.Integer, db.ForeignKey('perfumes.id'), primary_key=True),
    db.Column('note_id', db.Integer, db.ForeignKey('notes.id'), primary_key=True)
)

perfume_category = db.Table(
    'perfume_category',
    db.Column('perfume_id', db.Integer, db.ForeignKey('perfumes.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
    
)

class Perfume(db.Model):
    __tablename__ = 'perfumes'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100), nullable=False)

    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'))
    brand = db.relationship('Brand', backref='perfumes')

    categories = db.relationship('Category', secondary=perfume_category, backref='perfumes')
    comments = db.relationship('Comment', backref='perfume', lazy='dynamic')

    notes = db.relationship('Note', backref='perfume', lazy='dynamic')

