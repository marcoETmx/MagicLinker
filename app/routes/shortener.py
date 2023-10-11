from flask import abort, redirect, request
from flask_restx import Namespace, Resource, fields

from app.forms.forms import ShortenRequestForm
from app.services.shorten_service import create_shortened_url, get_original_url

shortener_ns = Namespace(
    "shortener", description="Operaciones relacionadas con el acortamiento de URLs"
)

url_model = shortener_ns.model(
    "URL",
    {
        "url": fields.String(required=True, description="URL original a acortar"),
        "short_code": fields.String(description="Código corto personalizado"),
    },
)


@shortener_ns.route("/shorten")
class ShortenURLResource(Resource):
    @shortener_ns.expect(url_model)
    @shortener_ns.response(201, "URL acortada con éxito")
    @shortener_ns.response(400, "Validación fallida")
    def post(self):
        form = ShortenRequestForm(data=request.get_json())

        if form.validate():
            try:
                shorten_url = create_shortened_url(form.data)
                return {"shorten_url": shorten_url}, 201
            except ValueError as e:
                shortener_ns.abort(400, errors=str(e))
        else:
            shortener_ns.abort(400, errors=form.errors)


@shortener_ns.route("/<string:short_code>")
class RedirectResource(Resource):
    @shortener_ns.response(302, "Redirección a la URL original")
    @shortener_ns.response(404, "URL corta no encontrada")
    def get(self, short_code):
        url_entry = get_original_url(short_code)
        if url_entry:
            return redirect(url_entry.original_url)

        abort(404, description="Shortened URL not found")
