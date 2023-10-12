from flask import Flask
from flask_restx import Api

from app.extensions import db
from app.routes.root import root_ns
from app.routes.shortener import shortener_ns
from config import Config, TestConfig


def create_app(config_name: str = None):
    app = Flask(__name__)

    if config_name == "config.TestConfig":
        app.config.from_object(TestConfig)
    else:
        app.config.from_object(Config)

    api = Api(
        version="1.0",
        title="API de MagicLinker",
        doc="/doc/",
        description="Documentación de la API de MagicLinker",
    )
    api.add_namespace(root_ns, path="/")
    api.add_namespace(shortener_ns, path="/shortener")
    api.init_app(app)

    db.init_app(app)

    return app
