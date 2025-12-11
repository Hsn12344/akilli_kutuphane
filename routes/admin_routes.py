from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from utils.decorators import admin_required
from services.admin_service import list_all_users, make_user_admin, create_admin_user

admin_bp = Blueprint('admin_bp', __name__)


# ------------------------------
# Mevcut kullanıcıyı admin yapma
# POST /admin/make-admin
# ------------------------------
@admin_bp.route('/make-admin', methods=['POST'])
@admin_required
def make_admin():
    data = request.get_json() or {}
    email = data.get("email")

    if not email:
        return jsonify({"message": "Email zorunlu."}), 400

    user, err = make_user_admin(email)
    if err:
        return jsonify({"message": err}), 400

    return jsonify({"message": f"{user.email} artık admin."}), 200


# ------------------------------
# Yeni admin oluşturma
# POST /admin/create-admin
# ------------------------------
@admin_bp.route('/create-admin', methods=['POST'])
@admin_required
def create_admin():
    data = request.get_json() or {}

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not all([name, email, password]):
        return jsonify({"message": "name, email ve password zorunludur."}), 400

    user, err = create_admin_user(name, email, password)
    if err:
        return jsonify({"message": err}), 400

    return jsonify({"message": f"{user.name} admin olarak oluşturuldu."}), 201


# ------------------------------
# Kullanıcıları listeleme
# GET /admin/users
# ------------------------------
@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_users():
    users = list_all_users()
    return jsonify(users), 200