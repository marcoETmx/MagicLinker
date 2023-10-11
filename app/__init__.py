from flask import Flask
from app.extensions import db
from flask_restx import Api
from app.routes.shortener import shortener_ns


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

    api = Api(
        version="1.0",
        title="API de MagicLinker",
        doc="/doc/",
        description="Documentación de la API de MagicLinker",
    )
    api.init_app(app)
    api.add_namespace(shortener_ns, path="/")

    db.init_app(app)

    return app
