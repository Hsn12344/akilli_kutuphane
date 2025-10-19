import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key")

    # MySQL bağlantısı
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Hasan1905#@localhost/kutuphane_db"

    # Mail ayarları
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'mail@example.com'  # kendi mailini yaz
    MAIL_PASSWORD = 'uygulama_şifresi'  # Google uygulama şifresi
