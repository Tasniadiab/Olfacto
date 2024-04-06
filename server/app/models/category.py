from app.models import db
from app.models.perfume import perfume_category, Perfume


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    
    perfumes = db.relationship('Perfume', secondary=perfume_category, backref='perfume_categories')