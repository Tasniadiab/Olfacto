from sqlalchemy import types
from app.models import db
from app.models.perfume import Perfume


class Brand(db.Model):
    __tablename__ = 'brands'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100), nullable=False)
    logo = db.Column(types.LargeBinary)

    perfumes = db.relationship('Perfume', backref='brand_perfume')