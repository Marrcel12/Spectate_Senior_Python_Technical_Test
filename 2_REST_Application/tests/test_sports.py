import json
from datetime import datetime, timezone

import app.schemas as schema
from app.crud import create_event, create_sport


def test_create_sport(client):
    response = client.post(
        "api/sports/",
        data=json.dumps({"name": "Basketball", "slug": "basketball", "active": True}),
        content_type="application/json",
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Basketball"
    assert data["slug"] == "basketball"
    assert data["active"] is True


def test_create_sport_duplicate_slug(client):
    with client.application.app_context():
        create_sport(
            sport=schema.SportCreate(name="Soccer", slug="soccer", active=True)
        )

    response = client.post(
        "api/sports/",
        data=json.dumps({"name": "Soccer", "slug": "soccer", "active": True}),
        content_type="application/json",
    )
    assert response.status_code == 400


def test_update_sport(client):
    with client.application.app_context():
        sport = create_sport(
            sport=schema.SportCreate(name="Tennis", slug="tennis", active=True)
        )

    response = client.put(
        f"api/sports/{sport.id}",
        data=json.dumps({"name": "Tennis Updated", "active": False}),
        content_type="application/json",
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Tennis Updated"
    assert data["active"] is False


def test_update_nonexistent_sport(client):
    response = client.put(
        "api/sports/9999",
        data=json.dumps({"name": "Nonexistent Sport", "active": False}),
        content_type="application/json",
    )
    assert response.status_code == 404


def test_get_sports(client):
    response = client.get("api/sports/")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


def test_get_sport_by_id(client):
    with client.application.app_context():
        sport = create_sport(
            sport=schema.SportCreate(name="Baseball", slug="baseball", active=True)
        )

    response = client.get(f"api/sports/{sport.id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Baseball"


def test_get_sports_with_filters(client):
    with client.application.app_context():
        create_sport(
            sport=schema.SportCreate(name="Hockey", slug="hockey", active=True)
        )

    response = client.get("api/sports/?name_regex=Hock")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Hockey"


def test_get_sports_by_active_status(client):
    with client.application.app_context():
        create_sport(
            sport=schema.SportCreate(
                name="Active Sport", slug="active-sport", active=True
            )
        )
        create_sport(
            sport=schema.SportCreate(
                name="Inactive Sport", slug="inactive-sport", active=False
            )
        )

    response = client.get("api/sports/?active=True")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert all(sport["active"] for sport in data)

    response = client.get("api/sports/?active=False")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert all(not sport["active"] for sport in data)


def test_get_sports_by_min_active_events(client):
    with client.application.app_context():
        sport = create_sport(
            sport=schema.SportCreate(
                name="Sport with Events", slug="sport-events", active=True
            )
        )
        for i in range(3):
            create_event(
                event=schema.EventCreate(
                    name=f"Event {i+1}",
                    type="preplay",
                    sport_id=sport.id,
                    scheduled_start=datetime.now(timezone.utc),
                )
            )

    response = client.get("api/sports/?min_active_events=2")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["name"] == "Sport with Events"


def test_sport_inactive_when_all_events_inactive(client):
    with client.application.app_context():
        sport = create_sport(
            sport=schema.SportCreate(name="Cricket", slug="cricket", active=True)
        )

        event1 = create_event(
            event=schema.EventCreate(
                name="Event 1",
                type="preplay",
                sport_id=sport.id,
                scheduled_start=datetime.now(timezone.utc),
            )
        )
        event2 = create_event(
            event=schema.EventCreate(
                name="Event 2",
                type="preplay",
                sport_id=sport.id,
                scheduled_start=datetime.now(timezone.utc),
            )
        )

    client.put(
        f"api/events/{event1.id}",
        data=json.dumps({"active": False}),
        content_type="application/json",
    )
    client.put(
        f"api/events/{event2.id}",
        data=json.dumps({"active": False}),
        content_type="application/json",
    )

    response = client.get(f"api/sports/{sport.id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["active"] is False


def test_invalid_sport_creation(client):
    response = client.post(
        "api/sports/",
        data=json.dumps({"name": 999, "slug": "invalid"}),
        content_type="application/json",
    )
    assert response.status_code == 400


def test_create_sport_missing_fields(client):
    response = client.post(
        "api/sports/",
        data=json.dumps({"name": "Basketball"}),
        content_type="application/json",
    )
    assert response.status_code == 400


def test_get_sports_by_complex_regex(client):
    with client.application.app_context():
        create_sport(
            sport=schema.SportCreate(name="Hockey", slug="hockey", active=True)
        )
        create_sport(
            sport=schema.SportCreate(
                name="Hockey League", slug="hockey-league", active=True
            )
        )
        create_sport(
            sport=schema.SportCreate(
                name="Hockey Championship League",
                slug="hockey-championship",
                active=True,
            )
        )
        create_sport(
            sport=schema.SportCreate(
                name="Hockey Championship", slug="hockey-championship", active=True
            )
        )

    response = client.get("api/sports/?name_regex=Hockey.*League")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "Hockey League"
    assert data[1]["name"] == "Hockey Championship League"
