📚 Akıllı Kütüphane Yönetim Sistemi

Akıllı Kütüphane, kullanıcıların kitapları dijital ortamda görüntüleyip ödünç alabileceği, yöneticilerin ise kitap, kategori, kullanıcı ve ceza süreçlerini merkezi olarak yönetebileceği tam kapsamlı bir kütüphane otomasyon sistemidir.

Proje; katmanlı mimari, rol bazlı yetkilendirme, JWT tabanlı kimlik doğrulama, mail bildirimleri, admin & user panelleri ve ceza yönetimi gibi modern yazılım mühendisliği yaklaşımlarıyla geliştirilmiştir.

🚀 Özellikler


👤 Kullanıcı Özellikleri

Kayıt olma ve giriş yapma (JWT)

Kitapları başlık / yazar / kategoriye göre arama

Kitap ödünç alma ve iade etme

Aktif, geciken ve toplam ödünç istatistikleri

Gecikme cezalarını görüntüleme ve ödeme

Hesap silme (admin hariç)

🛠️ Admin Özellikleri

Admin panel dashboard (istatistikler)

Kitap CRUD işlemleri

Kategori yönetimi

Kullanıcıları admin yapma

Tüm ödünç kayıtlarını görüntüleme ve zorla iade

Ceza yönetimi (ödendi / ödenmedi)

Admin aksiyonlarının loglanması (audit trail)


✉️ Mail Bildirimleri

Kayıt sonrası hoş geldin maili

Teslim tarihi hatırlatma maili

Gecikme cezası bilgilendirme maili

Asenkron (thread) mail gönderimi


🧠 Mimari Yapı

Proje katmanlı mimari (Layered Architecture) ile tasarlanmıştır:

routes        → API & page endpoint’leri
services      → İş mantığı (business logic)
repositories  → Veritabanı erişimi
models        → ORM (SQLAlchemy)
utils         → Decorator, mail, error handling
templates     → Jinja2 frontend
static        → JS / CSS / assets



Bu yapı:

Okunabilirliği artırır

Test edilebilirliği kolaylaştırır

Genişletilebilirliği sağlar


🛠️ Kullanılan Teknolojiler

Katman	Teknoloji
Backend	Python, Flask
ORM	SQLAlchemy
Auth	JWT (flask-jwt-extended)
Database	MySQL
Migration	Flask-Migrate
Mail	Flask-Mail
Frontend	Jinja2, Bootstrap 5, JavaScript
Security	Role-based access control
Architecture	Layered Architecture


🗄️Veritabanı Modelleri

User

Author

Category

Book

Borrow

Fine

AdminLog

Öne çıkan ilişkiler:

Kullanıcı → Ödünçler

Kitap → Ödünçler

Ödünç → Cezalar

Admin → AdminLog (audit trail)



🔐 Kimlik Doğrulama & Yetkilendirme

JWT token ile authentication

Token içinde role claim’i

Backend:

@jwt_required

@admin_required

Frontend:

Token expiration kontrolü

Rol bazlı sayfa yönlendirme



📡 API Genel Yapısı
Auth

POST /auth/register

POST /auth/login

DELETE /auth/delete-account

Books

GET /books

GET /books/search

POST /books (admin)

PUT /books/<id> (admin)

DELETE /books/<id> (admin)

Borrow & Fine

POST /borrow

POST /borrow/return/<id>

GET /borrow/borrows

GET /borrow/my-fines

POST /borrow/pay-fine/<id>

Admin

POST /api/admin/make-admin

GET /api/admin/users

GET /api/admin/logs





⚙️ Kurulum

1️⃣ Ortam Değişkenleri (.env)

SECRET_KEY=your_secret_key

JWT_SECRET_KEY=your_jwt_secret


DB_USER=root

DB_PASSWORD=1234

DB_HOST=localhost

DB_NAME=akilli_kutuphane



MAIL_SERVER=smtp.gmail.com

MAIL_PORT=587

MAIL_USE_TLS=True

MAIL_USERNAME=example@gmail.com

MAIL_PASSWORD=app_password



2️⃣ Bağımlılıkları Yükle

pip install -r requirements.txt



3️⃣ Veritabanını Oluştur

flask db init

flask db migrate

flask db upgrade



4️⃣ Uygulamayı Çalıştır

python app.py



🧪 Test & Kullanım

Frontend üzerinden tam akış test edilebilir

Postman ile API testleri yapılabilir

JWT expiration ve rol kontrolleri aktif



📌 Geliştirilebilir Alanlar

Pagination & caching

Raporlama ekranları

Kitap rezervasyon sistemi

PDF / Excel export

Docker desteği

Unit & integration testler



👤 Geliştirici

Akıllı Kütüphane Yönetim Sistemi
Yazılım Mühendisliği Projesi
Flask • MySQL • JWT • Layered Architecture
