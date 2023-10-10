from flask import Flask
from app.extensions import db
from app.routes.shortener import shortener


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

    db.init_app(app)

    app.register_blueprint(shortener)

    return app
