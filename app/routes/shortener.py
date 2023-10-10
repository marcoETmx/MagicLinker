from flask import jsonify, request, blueprints, redirect, abort
from app.services.shorten_service import create_shortened_url, get_original_url

shortener = blueprints.Blueprint("shortener", __name__)


@shortener.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()
    original_url = data.get("url")
    if not original_url:
        return jsonify(message="URL is required"), 400

    shorten_url = create_shortened_url(original_url)
    return jsonify(shorten_url=shorten_url), 201


@shortener.route("/<short_code>", methods=["GET"])
def redirect_to_original(short_code: str):
    url_entry = get_original_url(short_code)
    if url_entry:
        return redirect(url_entry.original_url)
    else:
        abort(404, description="Shortened URL not found")
