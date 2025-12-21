from models import db, Book, Author, Category

class BookRepository:

    @staticmethod
    def get_all():
        return Book.query.all()

    @staticmethod
    def get_by_id(book_id):
        return Book.query.get(book_id)

    @staticmethod
    def search(title=None, author=None, category=None):
        query = Book.query.join(Author).join(Category)

        if title:
            query = query.filter(Book.title.ilike(f"%{title}%"))

        if author:
            query = query.filter(Author.name.ilike(f"%{author}%"))

        if category:
            query = query.filter(Category.name.ilike(f"%{category}%"))

        return query.all()

    @staticmethod
    def save(book):
        db.session.add(book)
        db.session.commit()

    @staticmethod
    def delete(book):
        db.session.delete(book)
        db.session.commit()

    @staticmethod
    def get_or_create_author(author_name):
        author = Author.query.filter_by(name=author_name).first()
        if not author:
            author = Author(name=author_name)
            db.session.add(author)
            db.session.commit()
        return author
