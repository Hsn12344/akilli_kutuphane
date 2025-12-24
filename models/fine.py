from .base import db

class Fine(db.Model):
    __tablename__ = "fine"

    id = db.Column(db.Integer, primary_key=True)

    borrow_id = db.Column(
        db.Integer,
        db.ForeignKey("borrow.id", ondelete="CASCADE"),
        nullable=False
    )

    amount = db.Column(db.Float, nullable=False)
    is_paid = db.Column(db.Boolean, default=False)
    paid_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "borrow_id": self.borrow_id,
            "amount": self.amount,
            "is_paid": self.is_paid,
            "paid_at": self.paid_at.strftime("%Y-%m-%d %H:%M:%S") if self.paid_at else None,
            "user_name": self.borrow.user.name if self.borrow else None,
            "user_email": self.borrow.user.email if self.borrow else None
        }
