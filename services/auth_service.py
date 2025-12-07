from models import db, User
from flask_jwt_extended import create_access_token
from utils.mail_service import send_welcome_email

def register_user(name, email, password, role="user"):
    if not name or not email or not password:
        return None, "Tüm alanlar zorunludur."

    if User.query.filter_by(email=email).first():
        return None, "Bu e-posta zaten kayıtlı."

    user = User(name=name, email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    send_welcome_email(email, name)
    return user, None


def login_user(email, password):
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return None, None, "E-posta veya şifre hatalı."

    token = create_access_token(identity=user.id, additional_claims={"role": user.role})
    return token, user, None


def create_admin_direct(email, password):
    if not email or not password:
        return None, "E-posta ve şifre zorunludur."

    if User.query.filter_by(email=email).first():
        return None, "Bu e-posta zaten kayıtlı."

    admin = User(name="Admin", email=email, role="admin")
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    return admin, None
