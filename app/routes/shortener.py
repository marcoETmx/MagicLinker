from flask import request
from flask_restx import Resource

from app.forms.forms import ShortenRequestForm
from app.namespaces import shortener_ns
from app.schemas.shorten import response_model, url_model
from app.services.shorten_service import (create_shortened_url, get_all_urls,
                                          get_url_by_short_code)


@shortener_ns.errorhandler(ValueError)
def handle_value_error(error):
    """Return a custom message and 400 status code"""
    return {"message": str(error)}, 400


@shortener_ns.route("/urls")
class URLListResource(Resource):
    @shortener_ns.expect(url_model)
    @shortener_ns.marshal_with(response_model, code=201)
    @shortener_ns.response(201, "URL successfully shortened")
    @shortener_ns.response(400, "Validation error")
    def post(self):
        """Create a new shortened URL"""
        form = ShortenRequestForm(data=request.get_json())
        if not form.validate():
            shortener_ns.abort(400, errors=form.errors)

        return create_shortened_url(form.data), 201

    @shortener_ns.marshal_list_with(url_model)
    def get(self):
        """Retrieve all shortened URLs"""
        urls = get_all_urls()
        return urls


@shortener_ns.route("/urls/<string:shorten_code>")
class URLDetailResource(Resource):
    @shortener_ns.marshal_with(url_model)
    @shortener_ns.response(404, "URL not found")
    @shortener_ns.response(200, "URL successfully retrieved")
    def get(self, shorten_code):
        """Retrieve a shortened URL"""
        shorten_url = get_url_by_short_code(shorten_code)
        if not shorten_url:
            shortener_ns.abort(404, "URL not found")
        return shorten_url
