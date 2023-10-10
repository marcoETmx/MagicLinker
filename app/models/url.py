from app import db


class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String, nullable=False)
    shorten_url = db.Column(db.String, unique=True, nullable=False)
