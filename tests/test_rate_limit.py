from app.dependencies import rate_limit
from tests.conftest import create_test_url


def test_requests_under_rate_limit(client, monkeypatch):
    monkeypatch.setattr(
        rate_limit,
        "RATE_LIMIT",
        5,
    )

    response = create_test_url(
        client,
        url="https://www.google.com",
    )

    assert response.status_code == 200

    created = response.json()

    short_path = created["short_url"]

    for i in range(5):
        response = client.get(
            short_path,
            follow_redirects=False,
        )
        
        assert response.status_code == 302