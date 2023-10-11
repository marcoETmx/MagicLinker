import pytest

from app import create_app, db
from app.models.url import URL
from app.services.shorten_service import create_shortened_url, get_original_url


@pytest.fixture
def client():
    app = create_app(config_name="config.TestConfig")
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()


def test_create_shortened_url(client):
    # Setup
    data = {"url": "http://example.com"}
    with client.application.app_context():
        # Action
        code = create_shortened_url(data)
        # Expected
        assert len(code) == 6
        assert URL.query.filter_by(shorten_code=code).first() is not None


def test_create_shortened_url_with_existing_short_code(client):
    # Setup
    existing_code = "test123"
    data = {"url": "http://example.com", "short_code": existing_code}
    with client.application.app_context():
        create_shortened_url(data)

    # Action
    with client.application.app_context():
        with pytest.raises(ValueError) as exc_info:
            create_shortened_url(
                {"url": "http://new-url.com", "short_code": existing_code}
            )

    # Expected
    assert str(exc_info.value) == "The provided short code already exists"


def test_get_original_url(client):
    with client.application.app_context():
        # Setup
        data = {"url": "http://example.com", "short_code": "abcdef"}
        create_shortened_url(data)
        # Action
        result = get_original_url("abcdef")
        # Expected
        assert result.original_url == "http://example.com"


def test_get_original_url_with_nonexistent_short_code(client):
    # Setup
    non_existent_code = "noexist"
    # Action
    with client.application.app_context():
        result = get_original_url(non_existent_code)
    # Expected
    assert result is None