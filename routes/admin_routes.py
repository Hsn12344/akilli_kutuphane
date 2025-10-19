from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from models import db, User
from functools import wraps


admin_bp = Blueprint('admin_bp', __name__)

def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get("role") != "admin":
            return jsonify({"message": "Admin yetkisi gerekli."}), 403
        return fn(*args, **kwargs)
    return wrapper

# Mevcut kullanıcıyı admin yapma
@admin_bp.route('/make-admin', methods=['POST'])
@admin_required
def make_admin():
    data = request.get_json()
    email = data.get("email")
    if not email:
        return jsonify({"message": "Email zorunludur."}), 400
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "Kullanıcı bulunamadı."}), 404
    user.role = "admin"
    db.session.commit()
    return jsonify({"message": f"{user.email} artık admin."}), 200

# Yeni admin oluşturma
@admin_bp.route('/create-admin', methods=['POST'])
@admin_required
def create_admin():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    if not all([name, email, password]):
        return jsonify({"message": "Tüm alanlar zorunludur."}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email zaten kayıtlı."}), 400
    user = User(name=name, email=email, role="admin")
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": f"{name} admin olarak oluşturuldu."}), 201
