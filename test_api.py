import requests

BASE_URL = "http://127.0.0.1:5000"

def test_home():
    r = requests.get(BASE_URL + "/")
    print("Ana sayfa:", r.text)

def test_create_book():
    payload = {"title": "Sefiller", "isbn": "1234567890"}
    r = requests.post(BASE_URL + "/books", json=payload)
    print("Kitap oluştur:", r.json())

def test_get_books():
    r = requests.get(BASE_URL + "/books")
    print("Kitaplar listesi:", r.json())

def test_create_user():
    payload = {"name": "Hasan", "email": "hasan@example.com"}
    r = requests.post(BASE_URL + "/users", json=payload)
    print("Kullanıcı oluştur:", r.json())

def test_get_users():
    r = requests.get(BASE_URL + "/users")
    print("Kullanıcılar listesi:", r.json())

def test_borrow_book():
    payload = {"user_id": 1, "book_id": 1}
    r = requests.post(BASE_URL + "/borrow", json=payload)
    print("Ödünç alındı:", r.json())

def test_get_borrows():
    r = requests.get(BASE_URL + "/borrow")
    print("Ödünç listesi:", r.json())

if __name__ == "__main__":
    test_home()
    test_create_book()
    test_get_books()
    test_create_user()
    test_get_users()
    test_borrow_book()
    test_get_borrows()
