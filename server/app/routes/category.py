from flask import Blueprint, jsonify, request
from app.models.category import Category
from app.models.perfume import Perfume, perfume_category
from app.models import db
from sqlalchemy.orm.exc import StaleDataError


categories = Blueprint('categories', __name__)

@categories.route("/categories", methods=["GET"])
def get_all_categories():
    all_categories = Category.query.all()

    categories = []

    for catergory in all_categories:
        category_data = {
            "id": catergory.id,
            "name": catergory.name
        }
        categories.append(category_data)

    return jsonify({
        "categories" : categories
    })

@categories.route("/categories/create", methods=["POST"])
def create_category():
    name = request.json["name"]

    existing_category = Category.query.filter_by(name=name).first()
    if existing_category:
        return jsonify({"error": f"{existing_category.name} already exists"})
    
    new_catergory = Category(name=name)

    db.session.add(new_catergory)
    db.session.commit()

    return jsonify({
        "id": new_catergory.id,
        "name": new_catergory.name
    })

@categories.route("/categories/update/<int:id>", methods=["PUT"])
def update_category(id):

    update = request.get_json()

    existing_category = Category.query.get(id)

    print(update)

    for key, value in update.items():
        setattr(existing_category, key, value)
    db.session.commit()

    return jsonify({
        "id": existing_category.id,
        "name": existing_category.name
    }), 200

@categories.route("/categories/delete/<int:id>", methods=["DELETE"])
def delete_category(id):
    category = Category.query.get(id)
    
    if category:
        # Delete entries from the association table
        print(category.id)
        for perfume in category.perfumes:
            print(perfume.id)
            db.session.execute(perfume_category.delete().where(
                (perfume_category.c.perfume_id == perfume.id) &
                (perfume_category.c.category_id == category.id)
            ))
        
        # Delete the category
        db.session.commit()
        db.session.delete(category)
        db.session.commit()
        
        return jsonify({"msg": "Category successfully deleted"}), 200
    else: 
        return jsonify({"msg": "No category found"}),404
