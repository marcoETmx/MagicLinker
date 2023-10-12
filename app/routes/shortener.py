from flask import request
from flask_restx import Resource

from app.forms.forms import ShortenRequestForm
from app.services.shorten_service import create_shortened_url
from app.namespaces import shortener_ns
from app.schemas.shorten import url_model


@shortener_ns.route("/url")
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
