from flask import Blueprint, request, jsonify
from repositories.user_repository import UserRepository
from services.auth_service import register_user, login_user, create_admin_direct, request_delete_account, \
    confirm_delete_account
from flask_jwt_extended import jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}

    user, msg = register_user(
        data.get("name"),
        data.get("email"),
        data.get("password"),
        data.get("role", "user")
    )

    if not user:
        return jsonify({"message": msg}), 400

    return jsonify({"message": msg}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    token, user, err = login_user(
        data.get("email"),
        data.get("password")
    )

    if err:
        return jsonify({"message": err}), 401

    return jsonify({"access_token": token, "role": user.role}), 200


@auth_bp.route("/create_admin", methods=["POST"])
def create_admin():
    data = request.get_json()

    admin, err = create_admin_direct(
        data.get("email"),
        data.get("password")
    )

    if err:
        return jsonify({"message": err}), 400

    return jsonify({"message": "Admin başarıyla oluşturuldu."}), 201

@auth_bp.route("/verify", methods=["POST"])
def verify_account():
    data = request.get_json()
    email = data.get("email")
    code = data.get("code")

    user = UserRepository.get_by_email(email)
    if not user:
        return jsonify({"message": "Kullanıcı bulunamadı."}), 404

    if user.verification_code != code:
        return jsonify({"message": "Doğrulama kodu hatalı."}), 400

    user.is_verified = True
    user.verification_code = None
    UserRepository.save(user)

    return jsonify({"message": "Hesap başarıyla doğrulandı."}), 200

@auth_bp.route("/request-delete", methods=["POST"])
@jwt_required()
def request_delete():
    user_id = get_jwt_identity()
    success, msg = request_delete_account(user_id)
    return jsonify({"message": msg}), 200 if success else 400


@auth_bp.route("/confirm-delete", methods=["POST"])
@jwt_required()
def confirm_delete():
    data = request.get_json()
    code = data.get("code")

    user_id = get_jwt_identity()
    success, msg = confirm_delete_account(user_id, code)

    return jsonify({"message": msg}), 200 if success else 400
