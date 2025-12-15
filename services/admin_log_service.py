from models import db, AdminLog
from flask import request

def log_admin_action(admin_id, action, target=None):
    try:
        ip = request.remote_addr

        log = AdminLog(
            admin_id=admin_id,
            action=action,
            target=target,
            ip_address=ip
        )

        db.session.add(log)
        db.session.commit()

    except Exception as e:
        print("Admin log kaydedilemedi:", e)

def list_admin_logs():
    return AdminLog.query.order_by(AdminLog.created_at.desc()).all()
