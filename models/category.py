from .base import db

class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    books = db.relationship(
        "Book",
        backref="category",
        lazy=True,
        cascade="all, delete",
        passive_deletes=True
    )

    def to_dict(self):
        return {"id": self.id, "name": self.name}
