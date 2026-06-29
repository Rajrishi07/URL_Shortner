from .conftest import client

def test_home_page():
    response = client.get("/")

    assert response.status_code == 200


def test_create_short_url():
    response = client.post(
        "/api/shorten",
        json={
            "url": "https://www.google.com"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "short_url" in data

def test_invalid_url():
    response = client.post(
        "/api/shorten",
        json={
            "url": "hello world"
        },
    )

    assert response.status_code == 422

def test_redirect():
    create = client.post(
        "/api/shorten",
        json={
            "url": "https://www.wikipedia.org/"
        },
    )

    short_url = create.json()["short_url"]

    short_code = short_url.split("/")[-1]

    response = client.get(
        f"/{short_code}",
        follow_redirects=False,
    )

    assert response.status_code == 302

    assert response.headers["location"] == "https://www.wikipedia.org/"

def test_missing_short_code():
    response = client.get(
        "/thisdoesnotexist",
        follow_redirects=False,
    )

    assert response.status_code == 404