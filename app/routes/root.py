from flask import abort, redirect
from flask_restx import Resource

from app.namespaces import root_ns
from app.services.shorten_service import get_original_url


@root_ns.route("/<string:short_code>")
class RedirectResource(Resource):
    @root_ns.response(302, "Redirección a la URL original")
    @root_ns.response(404, "URL corta no encontrada")
    def get(self, short_code):
        url_entry = get_original_url(short_code)
        if url_entry:
            return redirect(url_entry.original_url)

        abort(404, description="Shortened URL not found")
