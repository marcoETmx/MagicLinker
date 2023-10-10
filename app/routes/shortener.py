from flask import jsonify, request, blueprints
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
    new_url = URL(original_url=original_url, shorten_url=shorten_url)
    db.session.add(new_url)
    db.session.commit()

    return jsonify(shorten_url=shorten_url), 201


@shortener.route("/<short_url>", methods=["GET"])
def redirect_to_original(short_url: str):
    return "Redirect to original URL"
