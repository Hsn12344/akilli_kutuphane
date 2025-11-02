from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models import db, Borrow, Book, Fine
from datetime import datetime, timedelta
from flask_mail import Message

borrow_bp = Blueprint('borrow_bp', __name__)

# Kitap ödünç alma
@borrow_bp.route('/borrow', methods=['POST'])
@jwt_required()
def borrow_book():
    user_id = get_jwt_identity()
    data = request.get_json()
    book_id = data.get("book_id")

    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Kitap bulunamadı."}), 404
    if book.available_copies < 1:
        return jsonify({"message": "Kitap stokta yok."}), 400

    # Aynı kullanıcı aynı kitabı zaten ödünç aldı mı kontrol et
    existing_borrow = Borrow.query.filter_by(user_id=user_id, book_id=book_id, return_date=None).first()
    if existing_borrow:
        return jsonify({"message": "Bu kitabı zaten ödünç almışsınız."}), 400

    borrow = Borrow(
        user_id=user_id,
        book_id=book_id,
        borrow_date=datetime.utcnow(),
        due_date=datetime.utcnow() + timedelta(days=14)
    )
    book.available_copies -= 1

    db.session.add(borrow)
    db.session.commit()
    return jsonify(borrow.to_dict()), 201

# Kitap iade
@borrow_bp.route('/return/<int:borrow_id>', methods=['POST'])
@jwt_required()
def return_book(borrow_id):
    user_id = get_jwt_identity()
    borrow = Borrow.query.get(borrow_id)
    if not borrow:
        return jsonify({"message": "Ödünç kaydı bulunamadı."}), 404
    if borrow.user_id != user_id:
        return jsonify({"message": "Bu ödünç kaydına erişim yetkiniz yok."}), 403
    if borrow.return_date:
        return jsonify({"message": "Kitap zaten iade edilmiş."}), 400

    borrow.return_date = datetime.utcnow()
    if borrow.return_date > borrow.due_date:
        delay_days = (borrow.return_date - borrow.due_date).days
        fine_amount = delay_days * 2.0
        fine = Fine(borrow_id=borrow.id, amount=fine_amount)
        db.session.add(fine)

        # Mail bildirimi
        try:
            msg = Message(
                subject="📚 Geç iade bildirimi",
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[borrow.user.email],
                body=f"Merhaba {borrow.user.name}, '{borrow.book.title}' kitabını "
                     f"{delay_days} gün geç iade ettiniz. Ceza: {fine_amount}₺."
            )
            current_app.extensions['mail'].send(msg)
        except Exception as e:
            print("Mail gönderilemedi:", e)

    borrow.book.available_copies += 1
    db.session.commit()
    return jsonify(borrow.to_dict()), 200

# Kullanıcı bazlı ve admin bazlı borç listeleme
@borrow_bp.route('/borrows', methods=['GET'])
@jwt_required()
def get_borrows():
    user_id = get_jwt_identity()
    claims = get_jwt()
    if claims.get("role") == "admin":
        borrows = Borrow.query.all()
    else:
        borrows = Borrow.query.filter_by(user_id=user_id).all()
    return jsonify([b.to_dict() for b in borrows]), 200

# Ceza listeleme (admin)
@borrow_bp.route('/fines', methods=['GET'])
@jwt_required()
def get_fines():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"message": "Admin yetkisi gerekli."}), 403
    fines = Fine.query.all()
    return jsonify([f.to_dict() for f in fines]), 200
