from models import db, Borrow, Book, Fine

class BorrowRepository:

    @staticmethod
    def get_borrow_by_id(borrow_id):
        return Borrow.query.get(borrow_id)

    @staticmethod
    def get_active_borrow(user_id, book_id):
        return Borrow.query.filter_by(
            user_id=user_id,
            book_id=book_id,
            return_date=None
        ).first()

    @staticmethod
    def get_all_active_borrows():
        return Borrow.query.filter_by(return_date=None).all()

    @staticmethod
    def get_user_borrows(user_id):
        return Borrow.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_all_borrows():
        return Borrow.query.all()

    @staticmethod
    def save(borrow):
        db.session.add(borrow)
        db.session.commit()

    @staticmethod
    def get_book(book_id):
        return Book.query.get(book_id)

    @staticmethod
    def get_fine_by_borrow(borrow_id):
        return Fine.query.filter_by(borrow_id=borrow_id).first()

    @staticmethod
    def get_all_fines():
        return Fine.query.all()

    @staticmethod
    def get_user_unpaid_fines(user_id):
        return (
            Fine.query
            .join(Borrow)
            .filter(
                Borrow.user_id == user_id,
                Fine.is_paid == False
            )
            .all()
        )

    @staticmethod
    def save_fine(fine):
        db.session.add(fine)
        db.session.commit()
