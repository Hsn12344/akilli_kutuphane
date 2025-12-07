from models import db, Book, Author, Category

def list_books():
    return Book.query.all()

def search_books(title, category):
    query = Book.query
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if category:
        query = query.join(Book.category).filter(Category.name.ilike(f"%{category}%"))
    return query.all()

def add_book_service(title, isbn, author_name, category_id, copies):
    if not all([title, isbn, author_name, category_id]):
        return None, "Başlık, ISBN, yazar adı ve kategori zorunludur."

    author = Author.query.filter_by(name=author_name).first()
    if not author:
        author = Author(name=author_name)
        db.session.add(author)
        db.session.commit()

    book = Book(
        title=title,
        isbn=isbn,
        author_id=author.id,
        category_id=category_id,
        available_copies=copies
    )

    db.session.add(book)
    db.session.commit()
    return book, None


def update_book_service(book_id, data):
    book = Book.query.get(book_id)
    if not book:
        return None, "Kitap bulunamadı."

    book.title = data.get("title", book.title)
    book.isbn = data.get("isbn", book.isbn)
    book.author_id = data.get("author_id", book.author_id)
    book.category_id = data.get("category_id", book.category_id)
    book.available_copies = data.get("available_copies", book.available_copies)
    db.session.commit()
    return book, None


def delete_book_service(book_id):
    book = Book.query.get(book_id)
    if not book:
        return False, "Kitap bulunamadı."

    db.session.delete(book)
    db.session.commit()
    return True, None
