import pytest

from app import create_app, db
from app.models.url import URL
from app.services.shorten_service import (
    create_shortened_url,
    get_all_urls,
    get_original_url,
    get_url_by_short_code,
)


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
        new_shortened = create_shortened_url(data)
        # Expected
        assert len(new_shortened.shorten_code) == 6
        assert (
            URL.query.filter_by(shorten_code=new_shortened.shorten_code).first()
            is not None
        )


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


def test_get_all_urls_function(client):
    with client.application.app_context():
        # Setup
        url1 = {"url": "http://example1.com", "short_code": "ijkl56"}
        url2 = {"url": "http://example2.com", "short_code": "mnop78"}
        create_shortened_url(url1)
        create_shortened_url(url2)

        # Action
        urls = get_all_urls()

        # Expected
        assert len(urls) == 2


def test_get_url_by_short_code_existing_code(client):
    # Setup
    with client.application.app_context():
        original_url = "http://example.com"
        shorten_code = "exmpl"
        url = {"url": original_url, "short_code": shorten_code}
        create_shortened_url(url)

        # Action
        result = get_url_by_short_code(shorten_code)

        # Expected
        assert result.original_url == original_url
        assert result.shorten_code == shorten_code


def test_get_url_by_short_code_non_existing_code(client):
    with client.application.app_context():
        # Action
        result = get_url_by_short_code("nonexist")

        # Expected
        assert result is None
