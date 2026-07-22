from app.exceptions.codes import ErrorCode
from tests.conftest import create_test_url
from datetime import datetime, timezone

def test_dashboard_empty(client):
    response = client.get("/api/dashboard")

    assert response.status_code == 200

    body = response.json()

    assert body["total_urls"] == 0
    assert body["active_urls"] == 0
    assert body["expired_urls"] == 0
    assert body["total_clicks"] == 0

    assert body["top_urls"] == []
    assert body["recent_urls"] == []
    
def test_get_dashboard(client):
    first = create_test_url(
        client,
        url="https://google.com",
        custom_alias="google",
    ).json()

    second = create_test_url(
        client,
        url="https://github.com",
        custom_alias="github",
    ).json()

    third = create_test_url(
        client,
        url="https://chatgpt.com",
        custom_alias="chatgpt",
    ).json()

    # google -> 3 clicks
    for _ in range(3):
        client.get(
            f"{first['short_url']}",
            follow_redirects=False,
        )

    # github -> 2 clicks
    for _ in range(2):
        client.get(
            f"{second['short_url']}",
            follow_redirects=False,
        )

    # chatgpt -> 1 click
    client.get(
        f"{third['short_url']}",
        follow_redirects=False,
    )

    response = client.get("/api/dashboard")

    assert response.status_code == 200

    body = response.json()
    print(f" { '%' * 100} \n{body}\n {'%' * 100}")

    assert body["total_urls"] == 3
    assert body["active_urls"] == 3
    assert body["expired_urls"] == 0
    assert body["total_clicks"] == 6

    assert len(body["top_urls"]) == 3
    assert len(body["recent_urls"]) == 3

    # Top URLs should be sorted by clicks
    assert body["top_urls"][0]["short_code"] == "google"
    assert body["top_urls"][0]["clicks"] == 3

    assert body["top_urls"][1]["short_code"] == "github"
    assert body["top_urls"][1]["clicks"] == 2

    assert body["top_urls"][2]["short_code"] == "chatgpt"
    assert body["top_urls"][2]["clicks"] == 1

    # Recent URLs should be sorted newest first
    assert body["recent_urls"][0]["id"] == third["id"]
    assert body["recent_urls"][1]["id"] == second["id"]
    assert body["recent_urls"][2]["id"] == first["id"]

