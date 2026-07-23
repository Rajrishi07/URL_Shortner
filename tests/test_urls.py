
def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200


def test_create_short_url_without_expiration(client):
    response = client.post(
        "/api/shorten",
        json={
            "url": "https://www.google.com"
        },
    )

    assert response.status_code == 200
    assert response.json()["expires_at"] is None

    data = response.json()

    assert "short_url" in data


def test_invalid_url(client):
    response = client.post(
        "/api/shorten",
        json={
            "url": "hello world"
        },
    )

    assert response.status_code == 422

def test_redirect(client):
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

def test_missing_short_code(client):
    response = client.get(
        "/thisdoesnotexist",
        follow_redirects=False,
    )

    assert response.status_code == 404

def test_create_custom_alias(client):
    response = client.post(
        "/api/shorten",
        json={
            "url": "https://github.com",
            "custom_alias": "github",
        },
    )

    assert response.status_code == 200

    assert response.json()["short_url"].endswith("/github")

def test_duplicate_alias(client):
    payload = {
        "url": "https://github.com",
        "custom_alias": "github",
    }

    client.post("/api/shorten", json=payload)

    response = client.post(
        "/api/shorten",
        json={
            "url": "https://google.com",
            "custom_alias": "github",
        },
    )

    assert response.status_code == 409

def test_create_short_url_with_expiration(client):
    response = client.post(
        "/api/shorten",
        json={
            "url": "https://www.blinkit.com",
            "expires_in_days": 5
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "short_url" in data
    assert data["expires_at"] is not None

def test_invalid_expiration_days(client):
    response = client.post(
        "/api/shorten",
        json={
            "url": "https://www.blinkit2.com",
            "expires_in_days": -1
        },
    )

    assert response.status_code == 422

