from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from services.borrow_service import (
    borrow_book_service,
    return_book_service,
    list_borrows,
    list_fines
)

borrow_bp = Blueprint('borrow_bp', __name__)

# ✅ POST /borrow
@borrow_bp.route('/', methods=['POST'])
@jwt_required()
def borrow_book():
    user_id = get_jwt_identity()
    data = request.get_json()

    borrow, err = borrow_book_service(user_id, data.get("book_id"))
    if err:
        return jsonify({"message": err}), 400

    return jsonify(borrow.to_dict()), 201


# ✅ POST /borrow/return/<id>
@borrow_bp.route('/return/<int:borrow_id>', methods=['POST'])
@jwt_required()
def return_book(borrow_id):
    user_id = get_jwt_identity()

    borrow, err = return_book_service(user_id, borrow_id)
    if err:
        return jsonify({"message": err}), 400

    return jsonify(borrow.to_dict()), 200


# ✅ GET /borrow/borrows
@borrow_bp.route('/borrows', methods=['GET'])
@jwt_required()
def get_borrows():
    user_id = get_jwt_identity()
    claims = get_jwt()

    borrows = list_borrows(user_id, claims.get("role"))
    return jsonify([b.to_dict() for b in borrows]), 200


# ✅ GET /borrow/fines
@borrow_bp.route('/fines', methods=['GET'])
@jwt_required()
def get_fines():
    claims = get_jwt()
    fines = list_fines(claims.get("role"))

    if fines is None:
        return jsonify({"message": "Admin yetkisi gerekli."}), 403

    return jsonify([f.to_dict() for f in fines]), 200
