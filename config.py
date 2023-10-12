import os


class TestConfig:
    TESTING = True
    BASE_URL = os.environ.get("BASE_URL") or "http://test.com/"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Config:
    BASE_URL = os.environ.get("BASE_URL") or "http://127.0.0.1:5000/"
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
