from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from models import db, Category, Book
from functools import wraps

category_bp = Blueprint('category_bp', __name__)

def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get("role") != "admin":
            return jsonify({"message": "Admin yetkisi gerekli."}), 403
        return fn(*args, **kwargs)
    return wrapper

# Kategori listeleme
@category_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([c.to_dict() for c in categories]), 200

# Kategori ekleme (admin)
@category_bp.route('/categories', methods=['POST'])
@admin_required
def add_category():
    data = request.get_json()
    name = data.get("name")
    if not name:
        return jsonify({"message": "Kategori adı zorunludur."}), 400

    if Category.query.filter_by(name=name).first():
        return jsonify({"message": "Kategori zaten mevcut."}), 400

    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    return jsonify(category.to_dict()), 201

# Kategori güncelleme (admin)
@category_bp.route('/categories/<int:category_id>', methods=['PUT'])
@admin_required
def update_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"message": "Kategori bulunamadı."}), 404

    data = request.get_json()
    new_name = data.get("name")
    if not new_name:
        return jsonify({"message": "Kategori adı zorunludur."}), 400

    category.name = new_name
    db.session.commit()
    return jsonify(category.to_dict()), 200

# Kategori silme (admin)
@category_bp.route('/categories/<int:category_id>', methods=['DELETE'])
@admin_required
def delete_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"message": "Kategori bulunamadı."}), 404

    if Book.query.filter_by(category_id=category.id).first():
        return jsonify({"message": "Bu kategoriye bağlı kitaplar var, önce onları silin."}), 400

    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Kategori silindi."}), 200
