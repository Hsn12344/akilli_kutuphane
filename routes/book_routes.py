from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from models import db, Book, Author
from functools import wraps

book_bp = Blueprint('book_bp', __name__)

def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get("role") != "admin":
            return jsonify({"message": "Admin yetkisi gerekli."}), 403
        return fn(*args, **kwargs)
    return wrapper

# Kitap listeleme
@book_bp.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([b.to_dict() for b in books]), 200

# Kitap ekleme (admin)
@book_bp.route('/books', methods=['POST'])
@admin_required
def add_book():
    data = request.get_json()
    title = data.get("title")
    isbn = data.get("isbn")
    author_name = data.get("author_name")
    category_id = data.get("category_id")
    available_copies = data.get("available_copies", 1)

    if not all([title, isbn, author_name, category_id]):
        return jsonify({"message": "Başlık, ISBN, yazar adı ve kategori zorunludur."}), 400

    # Yazar var mı kontrol et, yoksa ekle
    author = Author.query.filter_by(name=author_name).first()
    if not author:
        author = Author(name=author_name)
        db.session.add(author)
        db.session.commit()

    book = Book(title=title, isbn=isbn, author_id=author.id,
                category_id=category_id, available_copies=available_copies)

    db.session.add(book)
    db.session.commit()
    return jsonify(book.to_dict()), 201

# Kitap güncelleme (admin)
@book_bp.route('/books/<int:book_id>', methods=['PUT'])
@admin_required
def update_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Kitap bulunamadı."}), 404

    data = request.get_json()
    book.title = data.get("title", book.title)
    book.isbn = data.get("isbn", book.isbn)
    book.author_id = data.get("author_id", book.author_id)
    book.category_id = data.get("category_id", book.category_id)
    book.available_copies = data.get("available_copies", book.available_copies)
    db.session.commit()
    return jsonify(book.to_dict()), 200

# Kitap silme (admin)
@book_bp.route('/books/<int:book_id>', methods=['DELETE'])
@admin_required
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Kitap bulunamadı."}), 404
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Kitap silindi."}), 200
