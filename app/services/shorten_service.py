import shortuuid
from app import db
from app.models.url import URL


def create_shortened_url(validated_data: dict):
    original_url = validated_data["url"]
    shorten_code = validated_data.get("short_code") or shortuuid.uuid()[:6]
    existing_code = get_original_url(shorten_code)

    if existing_code:
        raise ValueError("The provided short code already exists")

    new_url = URL(original_url=original_url, shorten_code=shorten_code)
    db.session.add(new_url)
    db.session.commit()
    return shorten_code


def get_original_url(short_code: str):
    return URL.query.filter_by(shorten_code=short_code).first()
