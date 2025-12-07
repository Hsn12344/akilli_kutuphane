from models import db, User

def make_user_admin(email):
    if not email:
        return None, "Email zorunludur."

    user = User.query.filter_by(email=email).first()
    if not user:
        return None, "Kullanıcı bulunamadı."

    user.role = "admin"
    db.session.commit()
    return user, None


def create_admin_user(name, email, password):
    if not all([name, email, password]):
        return None, "Tüm alanlar zorunludur."

    if User.query.filter_by(email=email).first():
        return None, "Email zaten kayıtlı."

    user = User(name=name, email=email, role="admin")
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user, None
