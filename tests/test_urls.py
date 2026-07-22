from app.exceptions.codes import ErrorCode
from tests.conftest import create_test_url


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200


def test_create_short_url_without_expiration(client):
    response = create_test_url(
        client,
        custom_alias="example99",
    )
    body = response.json()
    assert body["expires_at"] is None
    assert "short_url" in body


def test_invalid_url(client):
    response = client.post(
        "/api/shorten",
        json={
            "url": "hello world",
        },
    )

    assert response.status_code == 422


def test_redirect(client):
    response = create_test_url(
        client,
        url="https://www.wikipedia.org/",
    )

    created = response.json()
    short_code = created["short_url"].split("/")[-1]

    response = client.get(
        f"/{short_code}",
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["location"] == "https://www.wikipedia.org/"


def test_missing_short_code(client):
    response = client.get(
        "/thisdoesnotexist",
        follow_redirects=False,
    )

    assert response.status_code == 404


def test_create_custom_alias(client):
    created = create_test_url(
        client,
        url="https://github.com",
        custom_alias="github",
    ).json()

    assert created["short_url"].endswith("/github")


def test_duplicate_alias(client):
    create_test_url(
        client,
        url="https://github.com",
        custom_alias="github3",
    )

    response = client.post(
        "/api/shorten",
        json={
            "url": "https://google.com",
            "custom_alias": "github3",
        },
    )

    assert response.status_code == 409


def test_create_short_url_with_expiration(client):
    created = create_test_url(
        client,
        url="https://www.blinkit.com",
        expires_in_days=5,
    ).json()

    assert created["expires_at"] is not None
    assert "short_url" in created


def test_invalid_expiration_days(client):
    response = client.post(
        "/api/shorten",
        json={
            "url": "https://www.blinkit2.com",
            "expires_in_days": -1,
        },
    )

    assert response.status_code == 422


def test_get_url_by_id(client):
    created = create_test_url(
        client,
        url="https://chatgpt.com/",
        custom_alias="cgpt",
    ).json()

    response = client.get(f"/api/urls/{created['id']}")

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == created["id"]
    assert body["short_code"] == created["short_url"].split('/')[-1]
    assert body["expires_at"] == created["expires_at"]


def test_get_url_by_invalid_id(client):
    response = client.get(f"/api/urls/{2**31 - 1}")

    assert response.status_code == 404

    body = response.json()

    assert body["success"] is False
    assert body["error"]["code"] == ErrorCode.URL_NOT_FOUND