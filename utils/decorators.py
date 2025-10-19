from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("role") != "admin":
                return jsonify({"error": "Bu işlem için admin yetkisi gereklidir."}), 403
        except Exception:
            return jsonify({"error": "Geçersiz veya eksik token."}), 401
        return fn(*args, **kwargs)
    return wrapper

def json_errorhandler(app):
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "İstenen kaynak bulunamadı."}), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error": "Sunucu hatası meydana geldi."}), 500

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": "Geçersiz istek."}), 400

    return app
