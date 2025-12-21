from flask_jwt_extended import create_access_token
from repositories.user_repository import UserRepository
from models import User
from utils.mail_service import send_welcome_email


def register_user(name, email, password, role="user"):
    if not name or not email or not password:
        return None, "Tüm alanlar zorunludur."

    if UserRepository.get_by_email(email):
        return None, "Bu e-posta zaten kayıtlı."

    user = User(name=name, email=email, role=role)
    user.set_password(password)

    UserRepository.save(user)

    send_welcome_email(email, name)
    return user, None


def login_user(email, password):
    user = UserRepository.get_by_email(email)

    if not user or not user.check_password(password):
        return None, None, "E-posta veya şifre hatalı."

    token = create_access_token(
        identity=user.id,
        additional_claims={"role": user.role}
    )

    return token, user, None


def create_admin_direct(email, password):
    if not email or not password:
        return None, "E-posta ve şifre zorunludur."

    if UserRepository.get_by_email(email):
        return None, "Bu e-posta zaten kayıtlı."

    admin = User(name="Admin", email=email, role="admin")
    admin.set_password(password)

    UserRepository.save(admin)
    return admin, None

def delete_my_account(current_user_id):
    user = UserRepository.get_by_id(current_user_id)

    if not user:
        return False, "Kullanıcı bulunamadı."

    if user.role == "admin":
        return False, "Admin hesabı bu yöntemle silinemez."

    UserRepository.delete(user)
    return True, "Hesabınız başarıyla silindi."
