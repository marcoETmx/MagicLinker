from flask_restx import fields

from app.routes.shortener import shortener_ns

url_request_model = shortener_ns.model(
    "URLRequest",
    {
        "url": fields.String(required=True, description="URL original"),
        "shorten_code": fields.String(description="Short code"),
    },
)

url_model = shortener_ns.model(
    "URL",
    {
        "id": fields.Integer(description="ID"),
        "original_url": fields.String(description="URL original"),
        "shorten_code": fields.String(description="Short code"),
        "created_at": fields.DateTime(description="Date created"),
        "shorten_url": fields.String(description="URL shortened"),
        "usage_count": fields.Integer(description="Number of times used"),
    },
)

response_model = shortener_ns.model(
    "ShortenResponse",
    {
        "shorten_url": fields.String(description="URL shortened"),
        "shorten_code": fields.String(description="Short code"),
    },
)
