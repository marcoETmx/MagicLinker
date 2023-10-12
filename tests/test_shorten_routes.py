import json

import pytest

from app import create_app, db
from app.services.shorten_service import create_shortened_url


@pytest.fixture
def client():
    app = create_app(config_name="config.TestConfig")
    app.config.from_object("config.TestConfig")

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        db.session.remove()
        db.drop_all()


# Pruebas para la ruta POST /shorten
def test_post_shorten_valid_url_no_shortcode(client):
    # Action
    response = client.post(
        "/shortener/urls",
        data=json.dumps({"url": "http://example.com"}),
        content_type="application/json",
    )
    # Expected
    assert response.status_code == 201
    assert "shorten_url" in response.json


def test_post_shorten_valid_url_with_shortcode(client):
    # Action
    response = client.post(
        "/shortener/urls",
        data=json.dumps({"url": "http://example.com", "short_code": "exmpl"}),
        content_type="application/json",
    )
    # Expected
    assert response.status_code == 201
    assert response.json["shorten_code"] == "exmpl"


def test_post_shorten_valid_url_with_existing_shortcode(client):
    # Setup
    client.post(
        "/shortener/urls",
        data=json.dumps({"url": "http://example.com", "short_code": "exmpl"}),
        content_type="application/json",
    )
    # Action
    response = client.post(
        "/shortener/urls",
        data=json.dumps({"url": "http://example2.com", "short_code": "exmpl"}),
        content_type="application/json",
    )
    # Expected
    assert response.status_code == 400


def test_post_shorten_invalid_url(client):
    # Action
    response = client.post(
        "/shortener/urls",
        data=json.dumps({"url": "not_a_valid_url"}),
        content_type="application/json",
    )
    # Expected
    assert response.status_code == 400


def test_get_redirect_valid_shortcode(client):
    # Action
    client.post(
        "/shortener/urls",
        data=json.dumps({"url": "http://example.com", "short_code": "exmpl"}),
        content_type="application/json",
    )
    response = client.get("/exmpl")
    # Expected
    assert response.status_code == 302
    assert response.location == "http://example.com"


def test_get_redirect_invalid_shortcode(client):
    # Action
    response = client.get("/not_exist")
    # Expected
    assert response.status_code == 404


def test_get_all_urls_returns_all_shortened_urls(client):
    # Setup
    url1 = {"url": "http://example1.com", "short_code": "ijkl56"}
    url2 = {"url": "http://example2.com", "short_code": "mnop78"}
    with client.application.app_context():
        create_shortened_url(url1)
        create_shortened_url(url2)

    # Action
    response = client.get("/shortener/urls")
    data = response.get_json()

    # Expected
    assert response.status_code == 200
    assert len(data) == 2
    assert any(url["original_url"] == "http://example1.com" for url in data)
    assert any(url["original_url"] == "http://example2.com" for url in data)
