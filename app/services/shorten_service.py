import shortuuid
from app import db
from app.models.url import URL


def create_shortened_url(original_url):
    shorten_url = shortuuid.uuid()[:6]
    new_url = URL(original_url=original_url, shorten_code=shorten_url)
    db.session.add(new_url)
    db.session.commit()
    return shorten_url


def get_original_url(short_code):
    return URL.query.filter_by(shorten_code=short_code).first()
