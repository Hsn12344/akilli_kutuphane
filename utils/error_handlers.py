from flask import jsonify

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

    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify({"error": "Yetkisiz erişim."}), 401

    @app.errorhandler(403)
    def forbidden(e):
        return jsonify({"error": "Bu işlem için yetkiniz yok."}), 403

    return app
