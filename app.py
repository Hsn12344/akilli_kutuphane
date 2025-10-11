from flask import Flask, request, jsonify
from models import db, Book, User, Borrow
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

# --- Ana route ---
@app.route('/', methods=['GET'])
def home():
    return "Akıllı Kütüphane API çalışıyor! 🚀"

# --- Book CRUD ---
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([b.to_dict() for b in books]), 200

@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'message': 'title alanı zorunludur.'}), 400

    book = Book(title=data['title'], isbn=data.get('isbn'))
    db.session.add(book)
    db.session.commit()
    return jsonify(book.to_dict()), 201

# --- User CRUD ---
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users]), 200

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({'message': 'name ve email alanları zorunludur.'}), 400

    user = User(name=data['name'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

# --- Borrow işlemleri ---
@app.route('/borrow', methods=['POST'])
def borrow_book():
    data = request.get_json()
    if not data or 'user_id' not in data or 'book_id' not in data:
        return jsonify({'message': 'user_id ve book_id gerekli.'}), 400

    borrow = Borrow(user_id=data['user_id'], book_id=data['book_id'])
    db.session.add(borrow)
    db.session.commit()
    return jsonify(borrow.to_dict()), 201

@app.route('/borrow', methods=['GET'])
def get_borrows():
    borrows = Borrow.query.all()
    return jsonify([b.to_dict() for b in borrows]), 200

if __name__ == '__main__':
    app.run(debug=True)
