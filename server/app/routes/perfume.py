from flask import Flask, Blueprint, jsonify, request
from app.models.perfume import Perfume, Notes, perfume_note
from app.models.brand import Brand
from app.models import db


perfume = Blueprint('perfume', __name__)

@perfume.route("/perfumes", methods = ["GET"])
def get_perfumes():
    all_perfumes = Perfume.query.all()

    perfumes = []
    for perfume in all_perfumes:
        comments = []
        for comment in perfume.comments:
            comment_data = {
                "id": comment.id,
                "text": comment.text,
                "user_id": comment.user_id
            }
            comments.append(comment_data)
        notes = []
        for note in perfume.notes:
            note_data = {
                "id": note.id,
                "notes": note.note
            }
            notes.append(note_data)
        categories = []
        for category in perfume.categories:
            category_data = {
                "id": category.id,
                "name": category.name
            }
            categories.append(category_data)
        perfume_data = {
            "id": perfume.id,
            "name": perfume.name,
            "description": perfume.description,
            "brand": perfume.brand.name,
            "notes" : notes,
            "categories": categories,
            "comments": comments
        }
        perfumes.append(perfume_data)
    return jsonify({'perfumes': perfumes})

@perfume.route("/create_perfume", methods = ["POST"])
def create_perfumes():
    name = request.json["name"]
    description = request.json["description"]
    brand = request.json["brand"]
    notes = request.json["notes"]
    categories = request.json["categories"]
    comments = request.json["comments"]


    exist_name = Perfume.query.filter_by(name=name).first()
    existing_brand = Brand.query.filter_by(name=brand).first() 

    if not existing_brand: 
        return jsonify({"error": "brand does not exist"})
    elif exist_name and existing_brand:
        return jsonify({"error": f"{brand}'s {name} already exists"})
    else: 
        brand_id = existing_brand.id 

    

    new_perfume = Perfume(name=name, description=description, brand_id=brand_id)
    db.session.add(new_perfume)
    db.session.commit()

    for note in notes: 
        existing_note = Notes.query.filter_by(note=note).first() 
        if existing_note: 
            note_id = existing_note.id
            
            association = perfume_note.insert().values(perfume_id=new_perfume.id, note_id=note_id)
            db.session.execute(association)
        else: 
            new_note = Notes(note=note)
            db.session.add(new_note)
            db.session.commit()
    db.session.commit()
    new_notes = [{"note": note.note, "id": note.id} for note in new_perfume.notes]

    return jsonify({
            "id": new_perfume.id,
            "name": new_perfume.name,
            "description": new_perfume.description,
            "brand": new_perfume.brand.name,
            "notes" : new_notes,
            # "categories": new_perfume.categories,
            # "comments": new_perfume.comments
            }), 201

@perfume.route("/create_note", methods = ["POST"])
def create_note():
    note = request.json["note"]

    new_note = Notes(note=note)
    db.session.add(new_note)
    db.session.commit()

    return jsonify({
        "id": new_note.id,
        "notes": new_note.note
    }), 201


@perfume.route("/notes", methods = ["GET"])
def get_notes():
    all_notes = Notes.query.all()
    
    notes = []
    for note in all_notes:
        note_data = {
            "id": note.id,
            "note": note.note
        }
        notes.append(note_data)
    return jsonify({'notes': notes})


