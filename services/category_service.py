from models import db, Category, Book

def list_categories():
    return Category.query.all()

def add_category_service(name):
    if not name:
        return None, "Kategori adı zorunludur."

    if Category.query.filter_by(name=name).first():
        return None, "Kategori zaten mevcut."

    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    return category, None


def update_category_service(category_id, name):
    category = Category.query.get(category_id)
    if not category:
        return None, "Kategori bulunamadı."

    if not name:
        return None, "Kategori adı zorunludur."

    category.name = name
    db.session.commit()
    return category, None


def delete_category_service(category_id):
    category = Category.query.get(category_id)
    if not category:
        return False, "Kategori bulunamadı."

    if Book.query.filter_by(category_id=category.id).first():
        return False, "Bu kategoriye bağlı kitaplar var."

    db.session.delete(category)
    db.session.commit()
    return True, None
