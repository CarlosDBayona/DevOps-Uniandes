from . import db
from datetime import datetime


class Blacklist(db.Model):
    __tablename__ = 'blacklists'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, index=True)
    app_uuid = db.Column(db.String(255), nullable=True)
    blocked_reason = db.Column(db.String(1024), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)  # IPv4 or IPv6
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Blacklist {self.email}>'

