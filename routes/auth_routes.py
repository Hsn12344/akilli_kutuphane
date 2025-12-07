from flask import Blueprint, request, jsonify
from services.auth_service import register_user, login_user, create_admin_direct

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    user, err = register_user(
        data.get("name"),
        data.get("email"),
        data.get("password"),
        data.get("role", "user")
    )

    if err:
        return jsonify({"message": err}), 400

    return jsonify({"message": "Kullanıcı başarıyla kaydedildi."}), 201


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
