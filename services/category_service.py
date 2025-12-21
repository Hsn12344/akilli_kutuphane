from repositories.category_repository import CategoryRepository
from models import Category

def list_categories():
    return CategoryRepository.get_all()


def add_category_service(name):
    if not name:
        return None, "Kategori adı zorunludur."

    if CategoryRepository.get_by_name(name):
        return None, "Kategori zaten mevcut."

    category = Category(name=name)
    CategoryRepository.save(category)

    return category, None


def update_category_service(category_id, name):
    category = CategoryRepository.get_by_id(category_id)
    if not category:
        return None, "Kategori bulunamadı."

    if not name:
        return None, "Kategori adı zorunludur."

    category.name = name
    CategoryRepository.save(category)

    return category, None


def delete_category_service(category_id):
    category = CategoryRepository.get_by_id(category_id)
    if not category:
        return False, "Kategori bulunamadı."

    if CategoryRepository.has_books(category_id):
        return False, "Bu kategoriye bağlı kitaplar var."

    CategoryRepository.delete(category)
    return True, None
