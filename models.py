from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

# ---------------------------------------------------
# USER
# ---------------------------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), default="user")

    borrows = db.relationship(
        'Borrow',
        backref='user',
        lazy=True,
        cascade="all, delete",
        passive_deletes=True
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role
        }


# ---------------------------------------------------
# AUTHOR
# ---------------------------------------------------
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    books = db.relationship(
        'Book',
        backref='author',
        lazy=True,
        cascade="all, delete",
        passive_deletes=True
    )

    def to_dict(self):
        return {"id": self.id, "name": self.name}


# ---------------------------------------------------
# CATEGORY
# ---------------------------------------------------
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    books = db.relationship(
        'Book',
        backref='category',
        lazy=True,
        cascade="all, delete",
        passive_deletes=True
    )

    def to_dict(self):
        return {"id": self.id, "name": self.name}


# ---------------------------------------------------
# BOOK
# ---------------------------------------------------
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    isbn = db.Column(db.String(50), unique=True, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id', ondelete="CASCADE"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete="CASCADE"), nullable=False)
    available_copies = db.Column(db.Integer, default=1)

    borrows = db.relationship(
        'Borrow',
        backref='book',
        lazy=True,
        cascade="all, delete",
        passive_deletes=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "isbn": self.isbn,
            "author": self.author.name if self.author else None,
            "author_id": self.author_id,
            "category": self.category.name if self.category else None,
            "category_id": self.category_id,
            "available_copies": self.available_copies
        }


# ---------------------------------------------------
# BORROW
# ---------------------------------------------------
class Borrow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id', ondelete="CASCADE"), nullable=False)
    borrow_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    return_date = db.Column(db.DateTime, nullable=True)

    fines = db.relationship(
        'Fine',
        backref='borrow',
        lazy=True,
        cascade="all, delete",
        passive_deletes=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user": self.user.name,
            "user_email": self.user.email,
            "user_id": self.user_id,
            "book": self.book.title,
            "book_id": self.book_id,
            "borrow_date": self.borrow_date.strftime("%Y-%m-%d %H:%M:%S"),
            "due_date": self.due_date.strftime("%Y-%m-%d %H:%M:%S"),
            "return_date": self.return_date.strftime("%Y-%m-%d %H:%M:%S") if self.return_date else None
        }


# ---------------------------------------------------
# FINE
# ---------------------------------------------------
class Fine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    borrow_id = db.Column(db.Integer, db.ForeignKey('borrow.id', ondelete="CASCADE"), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {"id": self.id, "borrow_id": self.borrow_id, "amount": self.amount}
