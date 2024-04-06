from app.models import db


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'))
    perfume_id = db.Column(db.Integer, db.ForeignKey('perfumes.id'))

    user = db.relationship('User', back_populates='comments')
    perfume = db.relationship('Perfume', backref='comment_relations')


perfume_note = db.Table(
    'perfume_note',
    db.Column('perfume_id', db.Integer, db.ForeignKey('perfumes.id'), primary_key=True),
    db.Column('note_id', db.Integer, db.ForeignKey('notes.id'), primary_key=True)
)

perfume_category = db.Table(
    'perfume_category',
    db.Column('perfume_id', db.Integer, db.ForeignKey('perfumes.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
    
)

class Notes(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    note = db.Column(db.Text, unique=True, nullable=False)
    perfume = db.relationship('Perfume', secondary=perfume_note, backref='note_perfume')


class Perfume(db.Model):
    __tablename__ = 'perfumes'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    add = db.Column(db.String(60))
    name = db.Column(db.String(100), nullable=False)
    description =  db.Column(db.Text)
    test = db.Column(db.Text)

    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'))
    brand = db.relationship('Brand', backref='perfume_brand')

    categories = db.relationship('Category', secondary=perfume_category, backref='perfume_category')
    comments = db.relationship('Comment', backref='perfume_comment', lazy='dynamic')

    notes = db.relationship('Notes', secondary=perfume_note, backref='perfume_note')

