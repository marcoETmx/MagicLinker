import shortuuid
from flask import current_app

from app import db
from app.models.url import URL


def create_shortened_url(validated_data: dict):
    original_url = validated_data["url"]
    shorten_code = validated_data.get("short_code") or shortuuid.uuid()[:6]
    existing_code = get_original_url(shorten_code)
    base_url = current_app.config["BASE_URL"]

    if existing_code:
        raise ValueError("The provided short code already exists")

    new_url = URL(
        original_url=original_url,
        shorten_code=shorten_code,
        domain=base_url,
        shorten_url=f"{base_url}{shorten_code}",
    )
    db.session.add(new_url)
    db.session.commit()
    return new_url


def get_original_url(short_code: str):
    return URL.query.filter_by(shorten_code=short_code).first()


def get_all_urls():
    return URL.query.all()


def get_url_by_short_code(short_code: str):
    return URL.query.filter_by(shorten_code=short_code).first()


def increment_url_visits(url_entry: URL):
    url_entry.usage_count += 1
    db.session.commit()
