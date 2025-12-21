from repositories.book_repository import BookRepository
from models import Book

def list_books():
    return BookRepository.get_all()


def search_books(title=None, author=None, category=None):
    return BookRepository.search(title, author, category)


def add_book_service(title, isbn, author_name, category_id, copies):
    if not all([title, isbn, author_name, category_id]):
        return None, "Başlık, ISBN, yazar adı ve kategori zorunludur."

    author = BookRepository.get_or_create_author(author_name)

    book = Book(
        title=title,
        isbn=isbn,
        author_id=author.id,
        category_id=category_id,
        available_copies=copies
    )

    BookRepository.save(book)
    return book, None


def update_book_service(book_id, data):
    book = BookRepository.get_by_id(book_id)
    if not book:
        return None, "Kitap bulunamadı."

    book.title = data.get("title", book.title)
    book.isbn = data.get("isbn", book.isbn)
    book.author_id = data.get("author_id", book.author_id)
    book.category_id = data.get("category_id", book.category_id)
    book.available_copies = data.get("available_copies", book.available_copies)

    BookRepository.save(book)
    return book, None


def delete_book_service(book_id):
    book = BookRepository.get_by_id(book_id)
    if not book:
        return False, "Kitap bulunamadı."

    BookRepository.delete(book)
    return True, None
