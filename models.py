from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# Kitap modeli
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    isbn = db.Column(db.String(50), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'isbn': self.isbn
        }


# Kullanıcı modeli
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'email': self.email}


# Ödünç kitap işlemleri
class Borrow(db.Model):
    __tablename__ = 'borrows'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    borrow_date = db.Column(db.DateTime, default=datetime.utcnow)
    return_date = db.Column(db.DateTime, nullable=True)

    user = db.relationship('User', backref='borrows')
    book = db.relationship('Book', backref='borrows')

    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user.to_dict(),
            'book': self.book.to_dict(),
            'borrow_date': self.borrow_date,
            'return_date': self.return_date
        }
