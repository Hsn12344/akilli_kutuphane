from .base import db

class Book(db.Model):
    __tablename__ = "book"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    isbn = db.Column(db.String(50), unique=True, nullable=False)

    author_id = db.Column(
        db.Integer,
        db.ForeignKey("author.id", ondelete="CASCADE"),
        nullable=False
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("category.id", ondelete="CASCADE"),
        nullable=False
    )

    available_copies = db.Column(db.Integer, default=1)

    borrows = db.relationship(
        "Borrow",
        backref="book",
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
