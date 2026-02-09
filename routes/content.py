import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from database import db
from models import Content
from flask_jwt_extended import jwt_required

content_bp = Blueprint("content", __name__)

# ---------------- GET SECTION (PUBLIC) ----------------
@content_bp.route("/content/<section>", methods=["GET"])
def get_section(section):
    items = Content.query.filter_by(section=section).order_by(Content.position).all()

    data = []
    for i in items:
        data.append({
            "id": i.id,
            "title": i.title,
            "desc": i.desc,
            "img": i.img,
            "date": i.date,
            "location": i.location,
            "author": i.author,
            "year": i.year
        })

    return jsonify(data)


# ---------------- CREATE (PROTECTED) ----------------
@content_bp.route("/content/<section>", methods=["POST"])
@jwt_required()
def create(section):
    data = request.json

    item = Content(
        section=section,
        title=data.get("title"),
        desc=data.get("desc"),
        img=data.get("img"),
        date=data.get("date"),
        location=data.get("location"),
        author=data.get("author"),
        year=data.get("year"),
        position=data.get("position", 0)
    )

    db.session.add(item)
    db.session.commit()

    return jsonify({"message": "Created", "id": item.id})


# ---------------- UPDATE (PROTECTED) ----------------
@content_bp.route("/content/<int:id>", methods=["PUT"])
@jwt_required()
def update(id):
    item = Content.query.get(id)

    if not item:
        return jsonify({"message": "Item not found"}), 404

    data = request.json

    item.title = data.get("title")
    item.desc = data.get("desc")
    item.img = data.get("img")
    item.date = data.get("date")
    item.location = data.get("location")
    item.author = data.get("author")
    item.year = data.get("year")
    item.position = data.get("position", item.position)

    db.session.commit()
    return jsonify({"message": "Updated"})


# ---------------- DELETE (PROTECTED) ----------------
@content_bp.route("/content/<int:id>", methods=["DELETE"])
@jwt_required()
def delete(id):
    item = Content.query.get(id)

    if not item:
        return jsonify({"message": "Item not found"}), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({"message": "Deleted"})


# ---------------- IMAGE UPLOAD (PROTECTED) ----------------
@content_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload():

    if "file" not in request.files:
        return jsonify({"message": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"message": "Empty filename"}), 400

    filename = secure_filename(file.filename)

    save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)

    # ensure folder exists
    os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)

    file.save(save_path)

    return jsonify({
        "url": f"/uploads/{filename}"
    })
