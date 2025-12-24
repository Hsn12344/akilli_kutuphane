from datetime import datetime
from .base import db

class Borrow(db.Model):
    __tablename__ = "borrow"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False
    )

    book_id = db.Column(
        db.Integer,
        db.ForeignKey("book.id", ondelete="CASCADE"),
        nullable=False
    )

    borrow_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    return_date = db.Column(db.DateTime, nullable=True)

    fines = db.relationship(
        "Fine",
        backref="borrow",
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
