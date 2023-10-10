from flask import jsonify, request, blueprints, redirect, abort
from app.services.shorten_service import create_shortened_url, get_original_url
from app.forms.forms import ShortenRequestForm

shortener = blueprints.Blueprint("shortener", __name__)


@shortener.route("/shorten", methods=["POST"])
def shorten_url():
    form = ShortenRequestForm(data=request.get_json())

    if form.validate():
        try:
            shorten_url = create_shortened_url(form.data)
            return jsonify(shorten_url=shorten_url), 201
        except ValueError as e:
            return jsonify(errors=str(e)), 400
    else:
        return jsonify(errors=form.errors), 400


@shortener.route("/<short_code>", methods=["GET"])
def redirect_to_original(short_code: str):
    url_entry = get_original_url(short_code)
    if url_entry:
        return redirect(url_entry.original_url)
    else:
        abort(404, description="Shortened URL not found")
