from flask import Blueprint, request, jsonify
from utils.decorators import admin_required
from services.category_service import (
    list_categories,
    add_category_service,
    update_category_service,
    delete_category_service
)

category_bp = Blueprint('category_bp', __name__)

# GET /categories → Kategori listele
@category_bp.route('/', methods=['GET'])
def get_categories():
    categories = list_categories()
    return jsonify([c.to_dict() for c in categories]), 200


# POST /categories → Yeni kategori ekle
@category_bp.route('/', methods=['POST'])
@admin_required
def add_category():
    data = request.get_json()

    category, err = add_category_service(data.get("name"))
    if err:
        return jsonify({"message": err}), 400

    return jsonify(category.to_dict()), 201


# PUT /categories/<id> → Güncelle
@category_bp.route('/<int:category_id>', methods=['PUT'])
@admin_required
def update_category(category_id):
    data = request.get_json()

    category, err = update_category_service(category_id, data.get("name"))
    if err:
        return jsonify({"message": err}), 404

    return jsonify(category.to_dict()), 200


# DELETE /categories/<id> → Sil
@category_bp.route('/<int:category_id>', methods=['DELETE'])
@admin_required
def delete_category(category_id):
    ok, err = delete_category_service(category_id)
    if err:
        return jsonify({"message": err}), 400

    return jsonify({"message": "Kategori silindi."}), 200
