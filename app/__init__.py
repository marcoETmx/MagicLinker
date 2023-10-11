from flask import Flask
from flask_restx import Api

from app.extensions import db
from app.routes.shortener import shortener_ns

from config import TestConfig


def create_app(config_name: str):
    app = Flask(__name__)

    if config_name == "config.TestConfig":
        app.config.from_object(TestConfig)
    else:
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
