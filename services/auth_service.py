from flask_jwt_extended import create_access_token
from repositories.user_repository import UserRepository
from models import User
from utils.mail_service import send_welcome_email, send_delete_account_email
from datetime import datetime, timedelta
from utils.code_generator import generate_verification_code
from utils.mail_service import send_verification_email
import random


def register_user(name, email, password, role="user"):
    if not name or not email or not password:
        return None, "Tüm alanlar zorunludur."

    if UserRepository.get_by_email(email):
        return None, "Bu e-posta zaten kayıtlı."

    code = generate_verification_code()

    user = User(
        name=name,
        email=email,
        role=role,
        is_verified=False,
        verification_code=code
    )
    user.set_password(password)
    UserRepository.save(user)

    send_verification_email(email, code)

    return user, "Doğrulama kodu e-posta adresinize gönderildi."

def login_user(email, password):
    user = UserRepository.get_by_email(email)

    if not user:
        return None, None, "E-posta veya şifre hatalı."

    if not user.is_verified:
        return None, None, "Hesap doğrulanmamış. Lütfen e-postanı kontrol et."

    if not user.check_password(password):
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

def request_delete_account(user_id):
    user = UserRepository.get_by_id(user_id)
    if not user:
        return False, "Kullanıcı bulunamadı."

    code = str(random.randint(100000, 999999))
    user.delete_code = code
    user.delete_code_expires = datetime.utcnow() + timedelta(minutes=10)

    UserRepository.save(user)

    send_delete_account_email(user.email, f"Hesap silme kodunuz: {code}")

    return True, "Doğrulama kodu e-posta adresinize gönderildi."


def confirm_delete_account(user_id, code):
    user = UserRepository.get_by_id(user_id)

    if not user:
        return False, "Kullanıcı bulunamadı."

    if user.delete_code != code:
        return False, "Kod hatalı."

    if datetime.utcnow() > user.delete_code_expires:
        return False, "Kodun süresi dolmuş."

    UserRepository.delete(user)
    return True, "Hesap başarıyla silindi."