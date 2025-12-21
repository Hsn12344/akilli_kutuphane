import json
import requests
import random

API_URL = "http://127.0.0.1:5000"
ADMIN_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2NjMxNzAzNiwianRpIjoiYmU5MzcxOTYtOTg5Ni00NmUwLWI5NWMtYTMzODU4MDA4ZGRiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzY2MzE3MDM2LCJjc3JmIjoiMTc3ZTdmNDEtOWQxZS00NWI1LWJmYTItY2ZhMmRmNjI1ODI3IiwiZXhwIjoxNzY2MzE3OTM2LCJyb2xlIjoiYWRtaW4ifQ._qrtIErlHQ0Cbj01b0IKrDMXsemD2NOWXh7jQyBAVG4"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {ADMIN_TOKEN}"
}

with open("books_seed.json", "r", encoding="utf-8") as f:
    books = json.load(f)

success = 0
failed = 0

for book in books:
    # ekstra güvenlik: stok random olsun istersek
    book["available_copies"] = random.randint(20, 50)

    res = requests.post(
        f"{API_URL}/books",
        headers=HEADERS,
        json=book
    )

    if res.status_code == 201:
        success += 1
        print(f"✔ Eklendi: {book['title']}")
    else:
        failed += 1
        print(f"✖ Hata: {book['title']} -> {res.text}")

print("\n=== SEED SONUCU ===")
print(f"Başarılı: {success}")
print(f"Hatalı   : {failed}")
