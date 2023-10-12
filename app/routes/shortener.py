from flask import request
from flask_restx import Resource

from app.forms.forms import ShortenRequestForm
from app.namespaces import shortener_ns
from app.schemas.shorten import response_model, url_list_model, url_model
from app.services.shorten_service import create_shortened_url, get_all_urls


@shortener_ns.errorhandler(ValueError)
def handle_value_error(error):
    """Return a custom message and 400 status code"""
    return {"message": str(error)}, 400


@shortener_ns.route("/urls")
class ShortenURLResource(Resource):
    @shortener_ns.expect(url_model)
    @shortener_ns.marshal_with(response_model, code=201)
    @shortener_ns.response(201, "URL shortened successfully")
    @shortener_ns.response(400, "Validation error")
    def post(self):
        """Create a shortened URL"""
        form = ShortenRequestForm(data=request.get_json())
        if not form.validate():
            shortener_ns.abort(400, errors=form.errors)

        new_url = create_shortened_url(form.data)
        return new_url, 201

    @shortener_ns.marshal_list_with(url_list_model)
    def get(self):
        """Get all shortened URLs"""
        urls = get_all_urls()
        return urls
