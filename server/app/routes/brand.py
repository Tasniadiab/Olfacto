from flask import Blueprint, jsonify, request
from app.models.brand import Brand
from app.models import db

brand = Blueprint('brand', __name__)

@brand.route("/brands", methods=["GET"])
def get_all_brands():
    all_brands = Brand.query.all()

    brands = []

    for brand in all_brands:
        brand_data = {
            "id": brand.id,
            "name": brand.name,
            "logo": brand.logo
        }
        brands.append(brand_data)

    return jsonify({
        "brands" : brands
    })

@brand.route("/brands/create", methods=["POST"])
def create_brand():
    name = request.json["name"]
    logo = request.json["logo"]

    existing_brand = Brand.query.filter_by(name=name).first()
    if existing_brand:
        return jsonify({"error": f"{existing_brand.name} already exists"})
    
    new_brand = Brand(name=name, logo=logo)

    db.session.add(new_brand)
    db.session.commit()

    return jsonify({
        "id": new_brand.id,
        "name": new_brand.name,
        "logo": new_brand.logo
    })