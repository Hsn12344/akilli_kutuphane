from flask import Flask, jsonify, send_from_directory
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_cors import CORS

from config import Config
from models import db
from utils.decorators import json_errorhandler
from routes.admin_routes import admin_bp
from routes.auth_routes import auth_bp
from routes.book_routes import book_bp
from routes.borrow_routes import borrow_bp
from routes.category_routes import category_bp

# -----------------------------
# Uygulama ayarları
# -----------------------------
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)
mail = Mail(app)
migrate = Migrate(app, db)
CORS(app)  # Frontend ile CORS hatası olmaması için

# -----------------------------
# Error handlers
# -----------------------------
json_errorhandler(app)

# -----------------------------
# Ana route
# -----------------------------
@app.route('/')
def home():
    return jsonify({"message": "Akıllı Kütüphane API çalışıyor!"})

# -----------------------------
# Frontend route
# -----------------------------
@app.route('/frontend')
def frontend():
    return app.send_static_file('frontend/index.html')

# -----------------------------
# Blueprint'leri register et
# -----------------------------
app.register_blueprint(admin_bp)
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(book_bp)
app.register_blueprint(borrow_bp)
app.register_blueprint(category_bp)

# -----------------------------
# DB oluştur
# -----------------------------
with app.app_context():
    db.create_all()

# -----------------------------
# Uygulamayı çalıştır
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
