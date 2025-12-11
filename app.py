from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_cors import CORS

from config import Config
from models import db
from utils.decorators import json_errorhandler

# API routes
from routes.auth_routes import auth_bp
from routes.book_routes import book_bp
from routes.borrow_routes import borrow_bp
from routes.category_routes import category_bp
from routes.admin_routes import admin_bp


# -------------------------------------------------
# APP INIT
# -------------------------------------------------
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)
mail = Mail(app)
migrate = Migrate(app, db)
CORS(app)

# Global JSON error handler
json_errorhandler(app)


# -------------------------------------------------
# FRONTEND ROUTES (HTML Pages)
# -------------------------------------------------

# Authentication pages
@app.route("/")
@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/register")
def register_page():
    return render_template("register.html")


# USER PANEL PAGES
@app.route("/user")
def user_dashboard():
    return render_template("user_dashboard.html")

@app.route("/user/books")
def user_books():
    return render_template("user_books.html")

@app.route("/user/borrows")
def user_borrows():
    return render_template("user_borrows.html")


# ADMIN PANEL PAGES
@app.route("/admin")
def admin_dashboard():
    return render_template("admin_dashboard.html")

@app.route("/admin/books")
def admin_books():
    return render_template("admin_books.html")

@app.route("/admin/categories")
def admin_categories():
    return render_template("admin_categories.html")

@app.route("/admin/users")
def admin_users():
    return render_template("admin_users.html")

@app.route("/admin/borrows")
def admin_borrows():
    return render_template("admin_borrows.html")

@app.route("/admin/fines")
def admin_fines():
    return render_template("admin_fines.html")


# -------------------------------------------------
# API BLUEPRINTS
# -------------------------------------------------
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(book_bp, url_prefix="/books")
app.register_blueprint(borrow_bp, url_prefix="/borrow")
app.register_blueprint(category_bp, url_prefix="/categories")
app.register_blueprint(admin_bp, url_prefix="/api/admin")


# -------------------------------------------------
# DATABASE INIT
# -------------------------------------------------
with app.app_context():
    db.create_all()


# -------------------------------------------------
# RUN APP
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
