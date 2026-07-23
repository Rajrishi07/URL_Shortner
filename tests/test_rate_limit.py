from app.dependencies import rate_limit

def test_requests_under_rate_limit(client, monkeypatch):
    monkeypatch.setattr(
        rate_limit,
        "RATE_LIMIT",
        5,
    )

    response = client.post(
        "/api/shorten",
        json={
            "url": "https://www.google.com",
        },
    )

    assert response.status_code == 200

    short_url = response.json()["short_url"]
    for _ in range(5):
        response = client.get(
            f"{short_url}",
            follow_redirects=False,
            )

        assert response.status_code == 302