from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from utils.decorators import admin_required
from services.admin_service import make_user_admin, create_admin_user

admin_bp = Blueprint('admin_bp', __name__)

# Mevcut kullanıcıyı admin yapma
@admin_bp.route('/make-admin', methods=['POST'])
@admin_required
def make_admin():
    data = request.get_json()
    email = data.get("email")

    user, err = make_user_admin(email)
    if err:
        return jsonify({"message": err}), 400

    return jsonify({"message": f"{user.email} artık admin."}), 200


# Yeni admin oluşturma
@admin_bp.route('/create-admin', methods=['POST'])
@admin_required
def create_admin():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    user, err = create_admin_user(name, email, password)
    if err:
        return jsonify({"message": err}), 400

    return jsonify({"message": f"{user.name} admin olarak oluşturuldu."}), 201
