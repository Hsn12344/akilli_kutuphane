from repositories.user_repository import UserRepository
from models import User


def make_user_admin(email):
    if not email:
        return None, "Email zorunludur."

    user = UserRepository.get_by_email(email)
    if not user:
        return None, "Kullanıcı bulunamadı."

    user.role = "admin"
    UserRepository.save(user)

    return user, None


def create_admin_user(name, email, password):
    if not all([name, email, password]):
        return None, "Tüm alanlar zorunludur."

    if UserRepository.get_by_email(email):
        return None, "Email zaten kayıtlı."

    user = User(name=name, email=email, role="admin")
    user.set_password(password)

    UserRepository.save(user)
    return user, None


def list_all_users():
    users = UserRepository.get_all()
    return [u.to_dict() for u in users]
