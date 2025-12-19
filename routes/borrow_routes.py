from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from services.borrow_service import (
    borrow_book_service,
    return_book_service,
    list_borrows,
    list_fines,
    list_user_fines,
    pay_fine_service,
    update_daily_fines
)

borrow_bp = Blueprint("borrow_bp", __name__)

@borrow_bp.route("/", methods=["POST"])
@jwt_required()
def borrow_book():
    user_id = get_jwt_identity()
    data = request.get_json()

    borrow, err = borrow_book_service(user_id, data.get("book_id"))
    if err:
        return jsonify({"message": err}), 400

    return jsonify(borrow.to_dict()), 201

@borrow_bp.route("/return/<int:borrow_id>", methods=["POST"])
@jwt_required()
def return_book(borrow_id):
    user_id = get_jwt_identity()

    borrow, err = return_book_service(user_id, borrow_id)
    if err:
        return jsonify({"message": err}), 400

    return jsonify(borrow.to_dict()), 200

@borrow_bp.route("/borrows", methods=["GET"])
@jwt_required()
def get_borrows():
    update_daily_fines()

    user_id = get_jwt_identity()
    role = get_jwt().get("role")

    borrows = list_borrows(user_id, role)
    return jsonify([b.to_dict() for b in borrows]), 200

@borrow_bp.route("/fines", methods=["GET"])
@jwt_required()
def get_fines():
    update_daily_fines()

    role = get_jwt().get("role")
    fines = list_fines(role)

    if fines is None:
        return jsonify({"message": "Admin yetkisi gerekli."}), 403

    return jsonify([f.to_dict() for f in fines]), 200

@borrow_bp.route("/my-fines", methods=["GET"])
@jwt_required()
def get_my_fines():
    user_id = get_jwt_identity()
    fines = list_user_fines(user_id)

    return jsonify([f.to_dict() for f in fines]), 200

@borrow_bp.route("/pay-fine/<int:fine_id>", methods=["POST"])
@jwt_required()
def pay_fine(fine_id):
    user_id = get_jwt_identity()

    ok, msg = pay_fine_service(user_id, fine_id)
    if not ok:
        return jsonify({"message": msg}), 400

    return jsonify({"message": msg}), 200
