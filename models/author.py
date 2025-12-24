from .base import db

class Author(db.Model):
    __tablename__ = "author"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    books = db.relationship(
        "Book",
        backref="author",
        lazy=True,
        cascade="all, delete",
        passive_deletes=True
    )

    def to_dict(self):
        return {"id": self.id, "name": self.name}
