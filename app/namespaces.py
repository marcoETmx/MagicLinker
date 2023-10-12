from flask_restx import Namespace

shortener_ns = Namespace(
    "shortener", description="Operations related to URL shortening"
)
root_ns = Namespace("root", description="Operations related to the root of the API")
