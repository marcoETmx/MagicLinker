from flask_restx import fields
from app.namespaces import shortener_ns

url_model = shortener_ns.model(
    "URL",
    {
        "url": fields.String(required=True, description="URL original a acortar"),
        "short_code": fields.String(description="Código corto personalizado"),
    },
)

response_model = shortener_ns.model(
    "ShortenResponse",
    {
        "shorten_url": fields.String(description="URL acortada completa"),
        "shorten_code": fields.String(
            description="Código corto generado o proporcionado"
        ),
    },
)
