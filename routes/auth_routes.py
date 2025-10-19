from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import db, User
from utils.mail_service import send_welcome_email

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "user")

    if not name or not email or not password:
        return jsonify({"message": "Tüm alanlar zorunludur."}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Bu e-posta zaten kayıtlı."}), 400

    user = User(name=name, email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    send_welcome_email(email, name)
    return jsonify({"message": "Kullanıcı başarıyla kaydedildi."}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"message": "E-posta veya şifre hatalı."}), 401

    access_token = create_access_token(identity=user.id, additional_claims={"role": user.role})
    return jsonify({"access_token": access_token, "role": user.role}), 200


@auth_bp.route("/create_admin", methods=["POST"])
def create_admin():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "E-posta ve şifre zorunludur."}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Bu e-posta zaten kayıtlı."}), 400

    admin = User(name="Admin", email=email, role="admin")
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()

    return jsonify({"message": "Admin başarıyla oluşturuldu."}), 201
