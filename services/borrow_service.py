from datetime import datetime, timedelta
from repositories.borrow_repository import BorrowRepository
from models import Borrow, Fine
from utils.mail_service import send_due_reminder

DAILY_FINE = 10.0

def borrow_book_service(user_id, book_id):
    book = BorrowRepository.get_book(book_id)

    if not book:
        return None, "Kitap bulunamadı."
    if book.available_copies < 1:
        return None, "Kitap stokta yok."

    existing = BorrowRepository.get_active_borrow(user_id, book_id)
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
    BorrowRepository.save(borrow)

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
    borrow = BorrowRepository.get_borrow_by_id(borrow_id)

    if not borrow:
        return None, "Ödünç kaydı bulunamadı."
    if borrow.user_id != user_id:
        return None, "Bu ödünce erişemezsiniz."
    if borrow.return_date:
        return None, "Kitap zaten iade edilmiş."

    borrow.return_date = datetime.utcnow()
    update_daily_fines()

    borrow.book.available_copies += 1
    BorrowRepository.save(borrow)

    return borrow, None

def list_borrows(user_id, role):
    update_daily_fines()

    if role == "admin":
        return BorrowRepository.get_all_borrows()

    return BorrowRepository.get_user_borrows(user_id)

def list_fines(role):
    if role != "admin":
        return None

    update_daily_fines()
    return BorrowRepository.get_all_fines()

def list_user_fines(user_id):
    update_daily_fines()
    return BorrowRepository.get_user_unpaid_fines(user_id)

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
    BorrowRepository.save_fine(fine)

    return True, "Ceza başarıyla ödendi."

def update_daily_fines():
    today = datetime.utcnow().date()
    borrows = BorrowRepository.get_all_active_borrows()

    for borrow in borrows:
        due = borrow.due_date.date()

        if today > due:
            days_late = (today - due).days
            expected_amount = days_late * DAILY_FINE

            fine = BorrowRepository.get_fine_by_borrow(borrow.id)

            if fine:
                fine.amount = expected_amount
                fine.is_paid = False
                fine.paid_at = None
            else:
                fine = Fine(
                    borrow_id=borrow.id,
                    amount=expected_amount,
                    is_paid=False
                )

            BorrowRepository.save_fine(fine)
