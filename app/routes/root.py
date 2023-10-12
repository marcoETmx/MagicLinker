from flask import abort, redirect
from flask_restx import Resource

from app.namespaces import root_ns
from app.services.shorten_service import get_original_url, increment_url_visits


@root_ns.route("/<string:short_code>")
class RedirectResource(Resource):
    @root_ns.response(302, "Redirecting to original URL")
    @root_ns.response(404, "URL not found")
    def get(self, short_code):
        """Redirect to original URL"""
        url_entry = get_original_url(short_code)
        if url_entry:
            increment_url_visits(url_entry)
            return redirect(url_entry.original_url)

        abort(404, description="Shortened URL not found")
