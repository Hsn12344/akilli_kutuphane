from models import db, Borrow, Book, Fine
from datetime import datetime, timedelta
from utils.mail_service import send_due_reminder

DAILY_FINE = 10.0  # Günlük ceza (TL)

def borrow_book_service(user_id, book_id):
    book = Book.query.get(book_id)

    if not book:
        return None, "Kitap bulunamadı."
    if book.available_copies < 1:
        return None, "Kitap stokta yok."

    existing = Borrow.query.filter_by(
        user_id=user_id,
        book_id=book_id,
        return_date=None
    ).first()

    if existing:
        return None, "Bu kitabı zaten ödünç almışsınız."

    due_date = datetime.utcnow() + timedelta(days=14)

    borrow = Borrow(
        user_id=user_id,
        book_id=book_id,
        borrow_date=datetime.utcnow(),
        due_date=due_date
    )

    book.available_copies -= 1
    db.session.add(borrow)
    db.session.commit()

    try:
        send_due_reminder(
            borrow.user.email,
            borrow.book.title,
            due_date
        )
    except Exception as e:
        print("Mail gönderilemedi:", e)

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

    # ❗ CEZA EKLENMEZ
    update_daily_fines()

    borrow.book.available_copies += 1
    db.session.commit()

    return borrow, None

def list_borrows(user_id, role):
    update_daily_fines()

    if role == "admin":
        return Borrow.query.all()

    return Borrow.query.filter_by(user_id=user_id).all()

def list_fines(role):
    if role != "admin":
        return None

    update_daily_fines()
    return Fine.query.all()

def list_user_fines(user_id):
    return (
        Fine.query
        .join(Borrow)
        .filter(
            Borrow.user_id == user_id,
            Fine.is_paid == False
        )
        .all()
    )

from datetime import datetime

def pay_fine_service(user_id, fine_id):
    fine = Fine.query.get(fine_id)
    if not fine:
        return False, "Ceza bulunamadı."

    if fine.borrow.user_id != user_id:
        return False, "Bu ceza size ait değil."

    if fine.is_paid:
        return False, "Bu ceza zaten ödenmiş."

    fine.is_paid = True
    fine.paid_at = datetime.utcnow()

    db.session.commit()
    return True, None

def update_daily_fines():
    today = datetime.utcnow().date()

    borrows = Borrow.query.filter_by(return_date=None).all()

    for borrow in borrows:
        due = borrow.due_date.date()

        if today > due:
            days_late = (today - due).days
            expected_amount = days_late * DAILY_FINE

            with db.session.no_autoflush:
                fine = Fine.query.filter_by(borrow_id=borrow.id).first()

            if fine:
                if fine.amount != expected_amount:
                    fine.amount = expected_amount
                    fine.is_paid = False
                    fine.paid_at = None
            else:
                fine = Fine(
                    borrow_id=borrow.id,
                    amount=expected_amount,
                    is_paid=False
                )
                db.session.add(fine)

    db.session.commit()
