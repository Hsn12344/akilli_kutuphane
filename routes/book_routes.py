from flask import Blueprint, request, jsonify
from utils.decorators import admin_required
from services.book_service import *

book_bp = Blueprint('book_bp', __name__)

# GET /books → KİTAP LİSTELE
@book_bp.route('/', methods=['GET'])
def get_books():
    books = list_books()
    return jsonify([b.to_dict() for b in books]), 200


# GET /books/search → ARAMA
@book_bp.route('/search', methods=['GET'])
def search():
    title = request.args.get('title', '')
    category = request.args.get('category', '')
    books = search_books(title, category)
    return jsonify([b.to_dict() for b in books]), 200


# POST /books → KİTAP EKLE
@book_bp.route('/', methods=['POST'])
@admin_required
def add_book():
    data = request.get_json()
    book, err = add_book_service(
        data.get("title"),
        data.get("isbn"),
        data.get("author_name"),
        data.get("category_id"),
        data.get("available_copies", 1)
    )
    if err:
        return jsonify({"message": err}), 400
    return jsonify(book.to_dict()), 201


@book_bp.route('/<int:book_id>', methods=['PUT'])
@admin_required
def update(book_id):
    book, err = update_book_service(book_id, request.get_json())
    if err:
        return jsonify({"message": err}), 404
    return jsonify(book.to_dict()), 200


@book_bp.route('/<int:book_id>', methods=['DELETE'])
@admin_required
def delete(book_id):
    ok, err = delete_book_service(book_id)
    if err:
        return jsonify({"message": err}), 404
    return jsonify({"message": "Kitap silindi."}), 200
