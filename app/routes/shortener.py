from flask import jsonify, request, blueprints, redirect, abort
import shortuuid
from app import db
from app.models.url import URL

shortener = blueprints.Blueprint("shortener", __name__)


@shortener.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()
    original_url = data.get("url")
    if not original_url:
        return jsonify(message="URL is required"), 400

    shorten_url = shortuuid.uuid()[:6]
    new_url = URL(original_url=original_url, shorten_code=shorten_url)
    db.session.add(new_url)
    db.session.commit()

    return jsonify(shorten_url=shorten_url), 201


@shortener.route("/<short_code>", methods=["GET"])
def redirect_to_original(short_code: str):
    url_entry = URL.query.filter_by(shorten_code=short_code).first()

    if url_entry:
        return redirect(url_entry.original_url)
    else:
        abort(404, description="Shortened URL not found")
