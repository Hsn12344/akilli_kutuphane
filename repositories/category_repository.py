from models import db, Category, Book

class CategoryRepository:

    @staticmethod
    def get_all():
        return Category.query.all()

    @staticmethod
    def get_by_id(category_id):
        return Category.query.get(category_id)

    @staticmethod
    def get_by_name(name):
        return Category.query.filter_by(name=name).first()

    @staticmethod
    def has_books(category_id):
        return Book.query.filter_by(category_id=category_id).first() is not None

    @staticmethod
    def save(category):
        db.session.add(category)
        db.session.commit()

    @staticmethod
    def delete(category):
        db.session.delete(category)
        db.session.commit()
