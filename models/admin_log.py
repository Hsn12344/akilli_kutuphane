from datetime import datetime
from .base import db

class AdminLog(db.Model):
    __tablename__ = "admin_log"

    id = db.Column(db.Integer, primary_key=True)

    admin_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete="SET NULL")
    )

    action = db.Column(db.String(255))
    target = db.Column(db.String(255))
    ip_address = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "admin": self.admin.name if self.admin else "Silinmiş Admin",
            "action": self.action,
            "target": self.target,
            "ip_address": self.ip_address,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
