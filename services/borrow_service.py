from models import db, Borrow, Book, Fine
from datetime import datetime, timedelta

def borrow_book_service(user_id, book_id):
    book = Book.query.get(book_id)
    if not book:
        return None, "Kitap bulunamadı."
    if book.available_copies < 1:
        return None, "Kitap stokta yok."

    existing = Borrow.query.filter_by(user_id=user_id, book_id=book_id, return_date=None).first()
    if existing:
        return None, "Bu kitabı zaten ödünç almışsınız."

    borrow = Borrow(
        user_id=user_id,
        book_id=book_id,
        borrow_date=datetime.utcnow(),
        due_date=datetime.utcnow() + timedelta(days=14)
    )

    book.available_copies -= 1
    db.session.add(borrow)
    db.session.commit()
    return borrow, None


def return_book_service(user_id, borrow_id):
    borrow = Borrow.query.get(borrow_id)
    if not borrow:
        return None, "Ödünç kaydı bulunamadı."
    if borrow.user_id != user_id:
        return None, "Bu ödünce erişemezsiniz."
    if borrow.return_date:
        return None, "Kitap zaten iade edilmiş."

    borrow.return_date = datetime.utcnow()

    if borrow.return_date > borrow.due_date:
        delay = (borrow.return_date - borrow.due_date).days
        fine = Fine(borrow_id=borrow.id, amount=delay * 2.0)
        db.session.add(fine)

    borrow.book.available_copies += 1
    db.session.commit()
    return borrow, None


def list_borrows(user_id, role):
    if role == "admin":
        return Borrow.query.all()
    return Borrow.query.filter_by(user_id=user_id).all()


def list_fines(role):
    if role != "admin":
        return None
    return Fine.query.all()
