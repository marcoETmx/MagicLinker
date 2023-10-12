from datetime import datetime

from app import db


class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String, nullable=False)
    shorten_code = db.Column(db.String, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    domain = db.Column(db.String, nullable=False)
    shorten_url = db.Column(db.String, nullable=False)
    usage_count = db.Column(db.Integer, default=0)
