from flask import Flask, Blueprint, jsonify, request
from app.models.perfume import Perfume, Notes, NoteType, perfume_note, perfume_category
from app.models.brand import Brand
from app.models.category import Category
from sqlalchemy.orm import selectinload
from app.models import db


perfume = Blueprint('perfume', __name__)

@perfume.route("/perfumes", methods = ["GET"])
def get_perfumes():
    all_perfumes = Perfume.query.options(selectinload(Perfume.notes).selectinload(Notes.note_types)).all()

    perfumes = []
    for perfume in all_perfumes:
        comments = []
        #try to optimize this later if you can 
        for comment in perfume.comments:
            comment_data = {
                "id": comment.id,
                "text": comment.text,
                "user_id": comment.user_id
            }
            comments.append(comment_data)
        notes = []
        top_notes = []
        heart_notes = []
        base_notes = []
        
        for perf_note in perfume.notes:
            note_data = {
                    "id": perf_note.id,
                    "notes": perf_note.note
                }
            for note_type in perf_note.note_types:
                if note_type.name == "Top Note":
                    top_notes.append(note_data)
                elif note_type.name == "Heart Note":
                    heart_notes.append(note_data)
                elif note_type.name == "Base Note":
                        base_notes.append(note_data)
                else: 
                    notes.append(note_data)
        notes.append({"Top Notes": top_notes})
        notes.append({"Heart Notes": heart_notes})
        notes.append({"Base Notes": base_notes})
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
    print(len(perfumes))
    return jsonify({'perfumes': perfumes})

@perfume.route("/perfumes/<int:id>", methods=["GET"])
def get_perfume(id):
    perfume = Perfume.query.get(id)

    query = db.session.query(Notes, NoteType) \
        .join(perfume_note, perfume_note.c.note_id == Notes.id) \
        .join(NoteType, perfume_note.c.note_type_id == NoteType.id) \
        .filter(perfume_note.c.perfume_id == id) \
        .all()

    perfume_data = {
        "id": perfume.id,
        "name": perfume.name,
        "description": perfume.description,
        "brand": perfume.brand.name,
        "categories": [],
        "comments": [],
        "notes": {"Top Notes": [], "Heart Notes": [], "Base Notes": [], "Other Notes": []}
    }

    for note, note_type in query:
        note_data = {"id": note.id, "note": note.note}
        if note_type.name == "Top Note":
            perfume_data["notes"]["Top Notes"].append(note_data)
        elif note_type.name == "Heart Note":
            perfume_data["notes"]["Heart Notes"].append(note_data)
        elif note_type.name == "Base Note":
            perfume_data["notes"]["Base Notes"].append(note_data)
        else:
            perfume_data["notes"]["Other Notes"].append(note_data)

    return jsonify({
        "id": perfume_data["id"],
        "name": perfume_data["name"],
        "description": perfume_data["description"],
        "brand": perfume_data["brand"],
        "notes": perfume_data["notes"]
    })

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
    elif exist_name is not None and existing_brand is not None:
        return jsonify({"error": f"{brand}'s {name} already exists"})
    else: 
        brand_id = existing_brand.id 

    new_perfume = Perfume(name=name, description=description, brand_id=brand_id)
    db.session.add(new_perfume)
    perfume_categories = []
    for category in categories: 
        existing_category = Category.query.filter_by(name=category).first()

        if not existing_category: 
            return jsonify({"error": " Category doesn't exist"})
        else: 
            category_id = existing_category.id
            association = perfume_category.insert().values(perfume_id=new_perfume.id, category_id=category_id)
            db.session.execute(association)
            perfume_categories.append({"name": existing_category.name, "id": category_id})
    
    new_notes = []
    top_notes = []
    heart_notes = []
    base_notes = []
    for note in notes: 
        note_name = note["note"]
        note_type_name = note["note_type"]
        existing_note = Notes.query.filter_by(note=note_name).first() 
        note_type = NoteType.query.filter_by(name=note_type_name).first()
        if existing_note: 
            note_id = existing_note.id
            
            association = perfume_note.insert().values(perfume_id=new_perfume.id, note_id=note_id, note_type_id=note_type.id)
            db.session.execute(association)
            note_data = {
                        "id": existing_note.id,
                        "notes": note_name
                    }
        else: 
            new_note = Notes(note=note_name)
            db.session.add(new_note)
            db.session.commit()
            note_id = new_note.id
            
            association = perfume_note.insert().values(perfume_id=new_perfume.id, note_id=note_id, note_type_id=note_type.id)
            db.session.execute(association)
            note_data = {
                        "id": note_id,
                        "notes": note_name
                    }
        if note_type_name == "Top Note":
            top_notes.append(note_data)
        elif note_type_name == "Heart Note":
            heart_notes.append(note_data)
        elif note_type_name == "Base Note":
            base_notes.append(note_data)
    new_notes.append({"Top Notes": top_notes})
    new_notes.append({"Heart Notes": heart_notes})
    new_notes.append({"Base Notes": base_notes})
    

    db.session.commit()
    

    return jsonify({
            "id": new_perfume.id,
            "name": new_perfume.name,
            "description": new_perfume.description,
            "brand": new_perfume.brand.name,
            "notes" : new_notes,
            "categories": perfume_categories,
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


