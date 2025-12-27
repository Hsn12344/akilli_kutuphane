from flask import Blueprint, request, jsonify
from utils.decorators import admin_required
from services.book_service import *
from models import db

book_bp = Blueprint('book_bp', __name__)

@book_bp.route('/', methods=['GET'])
def get_books():
    books = list_books()
    return jsonify([b.to_dict() for b in books]), 200

@book_bp.route('/search', methods=['GET'])
def search():
    title = request.args.get('title')
    category = request.args.get('category')
    author = request.args.get('author')

    books = search_books(
        title=title,
        category=category,
        author=author
    )

    return jsonify([b.to_dict() for b in books]), 200

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


@book_bp.route("/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    data = request.get_json()

    book = Book.query.get_or_404(book_id)

    if not data:
        return jsonify({"error": "Veri gönderilmedi"}), 400

    if "title" in data:
        book.title = data["title"]

    if "isbn" in data:
        book.isbn = data["isbn"]

    if "category_id" in data:
        try:
            book.category_id = int(data["category_id"])
        except ValueError:
            return jsonify({"error": "Kategori ID geçersiz"}), 400

    if "available_copies" in data:
        book.available_copies = int(data["available_copies"])

    db.session.commit()

    return jsonify({"message": "Kitap güncellendi"}), 200

@book_bp.route('/<int:book_id>', methods=['DELETE'])
@admin_required
def delete(book_id):
    ok, err = delete_book_service(book_id)
    if err:
        return jsonify({"message": err}), 404
    return jsonify({"message": "Kitap silindi."}), 200
