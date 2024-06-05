import json
from datetime import datetime, timedelta, timezone

import app.schemas as schema
from app.crud import create_event, create_selection, create_sport


def test_create_event(client):
    with client.application.app_context():
        sport = create_sport(
            sport=schema.SportCreate(name="Football", slug="football", active=True)
        )
    response = client.post(
        "api/events/",
        data=json.dumps(
            {
                "name": "Champions League Final",
                "type": "preplay",
                "sport_id": sport.id,
                "scheduled_start": datetime.now(timezone.utc).isoformat(),
            }
        ),
        content_type="application/json",
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Champions League Final"
    assert data["slug"] == "champions-league-final"
    assert data["type"] == "preplay"
    assert data["active"] is True


def test_update_event(client):
    with client.application.app_context():
        sport = create_sport(
            sport=schema.SportCreate(name="Football", slug="football", active=True)
        )
        event = create_event(
            event=schema.EventCreate(
                name="Bowl",
                type="preplay",
                sport_id=sport.id,
                scheduled_start=datetime.now(timezone.utc),
            )
        )

    response = client.put(
        f"api/events/{event.id}",
        data=json.dumps({"name": "Super Bowl", "status": "Started"}),
        content_type="application/json",
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Super Bowl"
    assert data["status"] == "Started"
    assert "actual_start" in data


def test_get_events(client):
    response = client.get("api/events/")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


def test_event_inactive_when_all_selections_inactive(client):
    with client.application.app_context():
        sport = create_sport(
            sport=schema.SportCreate(name="Football", slug="football", active=True)
        )
        event = create_event(
            event=schema.EventCreate(
                name="Event With Selections",
                type="preplay",
                sport_id=sport.id,
                scheduled_start=datetime.now(timezone.utc),
            )
        )
        selection = create_selection(
            selection=schema.SelectionCreate(
                name="Selection 1",
                event_id=event.id,
                price=1.5,
                active=True,
                outcome="Unsettled",
            )
        )

    # Make selection inactive
    client.put(
        f"api/selections/{selection.id}",
        data=json.dumps({"active": False}),
        content_type="application/json",
    )

    response = client.get(f"api/events/{event.id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["active"] is False


def test_search_events_by_name(client):
    with client.application.app_context():
        sport = create_sport(
            sport=schema.SportCreate(name="Football", slug="football", active=True)
        )
        create_event(
            event=schema.EventCreate(
                name="Unique Event Name",
                type="preplay",
                sport_id=sport.id,
                scheduled_start=datetime.now(timezone.utc),
            )
        )

    response = client.get("api/events/?name=Unique Event Name")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Unique Event Name"


def test_search_events_by_timeframe(client):
    with client.application.app_context():
        sport = create_sport(
            sport=schema.SportCreate(name="Football", slug="football", active=True)
        )
        create_event(
            event=schema.EventCreate(
                name="Future Event",
                type="preplay",
                sport_id=sport.id,
                scheduled_start=(
                    datetime.now(timezone.utc) + timedelta(days=1)
                ).isoformat(),
            )
        )

    start_time = (datetime.now(timezone.utc) + timedelta(hours=23)).isoformat(" ")
    end_time = (datetime.now(timezone.utc) + timedelta(hours=25)).isoformat(" ")

    response = client.get(
        f"api/events/?scheduled_start_gte={start_time}&scheduled_start_lte={end_time}"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Future Event"


def test_invalid_event_creation(client):
    response = client.post(
        "api/events/",
        data=json.dumps({"name": "", "type": "invalid", "sport_id": 9999}),
        content_type="application/json",
    )
    assert response.status_code == 400


def test_update_nonexistent_event(client):
    response = client.put(
        f"api/events/99999",
        data=json.dumps({"name": "Super Bowl", "status": "Started"}),
        content_type="application/json",
    )
    assert response.status_code == 404


def test_create_event_nonexistent_sport(client):
    response = client.post(
        "api/events/",
        data=json.dumps(
            {
                "name": "Invalid Event",
                "type": "preplay",
                "sport_id": 9999,
                "scheduled_start": datetime.now(timezone.utc).isoformat(),
            }
        ),
        content_type="application/json",
    )
    assert response.status_code == 404
    assert response.get_json()["error"] == "NotExistError"


def test_update_event_invalid_data_types(client):
    with client.application.app_context():
        sport = create_sport(
            sport=schema.SportCreate(name="Basketball", slug="basketball", active=True)
        )
        event = create_event(
            event=schema.EventCreate(
                name="Basketball Match",
                type="preplay",
                sport_id=sport.id,
                scheduled_start=datetime.now(timezone.utc),
            )
        )

    response = client.put(
        f"api/events/{event.id}",
        data=json.dumps({"name": 123, "status": "Started"}),
        content_type="application/json",
    )
    assert response.status_code == 400


def test_get_events_by_type(client):
    with client.application.app_context():
        sport = create_sport(
            sport=schema.SportCreate(name="Soccer", slug="soccer", active=True)
        )
        create_event(
            event=schema.EventCreate(
                name="Preplay Event",
                type="preplay",
                sport_id=sport.id,
                scheduled_start=datetime.now(timezone.utc),
            )
        )
        create_event(
            event=schema.EventCreate(
                name="Inplay Event",
                type="inplay",
                sport_id=sport.id,
                scheduled_start=datetime.now(timezone.utc),
            )
        )

    response = client.get("api/events/?type=preplay")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert all(event["type"] == "preplay" for event in data)

    response = client.get("api/events/?type=inplay")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert all(event["type"] == "inplay" for event in data)


def test_search_events_by_complex_name_regex(client):
    with client.application.app_context():
        sport = create_sport(
            sport=schema.SportCreate(name="Soccer", slug="soccer", active=True)
        )
        create_event(
            event=schema.EventCreate(
                name="International Soccer Cup",
                type="preplay",
                sport_id=sport.id,
                scheduled_start=datetime.now(timezone.utc),
            )
        )
        create_event(
            event=schema.EventCreate(
                name="National Soccer League",
                type="preplay",
                sport_id=sport.id,
                scheduled_start=datetime.now(timezone.utc),
            )
        )
        create_event(
            event=schema.EventCreate(
                name="Regional Soccer Tournament",
                type="preplay",
                sport_id=sport.id,
                scheduled_start=datetime.now(timezone.utc),
            )
        )

    response = client.get("api/events/?name_regex=Soccer\\sCup$")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "International Soccer Cup"

    response = client.get("api/events/?name_regex=Soccer\\s(L|T).*")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "National Soccer League"
    assert data[1]["name"] == "Regional Soccer Tournament"
