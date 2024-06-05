import json
from datetime import datetime, timezone

import app.schemas as schema
from app.crud import create_event, create_selection, create_sport


def test_create_selection(client):
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

    response = client.post(
        "api/selections/",
        data=json.dumps(
            {
                "name": "Team A wins",
                "event_id": event.id,
                "price": 1.5,
                "active": True,
                "outcome": "Unsettled",
            }
        ),
        content_type="application/json",
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Team A wins"
    assert data["price"] == 1.5
    assert data["active"] is True
    assert data["outcome"] == "Unsettled"


def test_update_selection(client):
    with client.application.app_context():
        sport = create_sport(
            sport=schema.SportCreate(name="Tennis", slug="tennis", active=True)
        )
        event = create_event(
            event=schema.EventCreate(
                name="Tennis Match",
                type="preplay",
                sport_id=sport.id,
                scheduled_start=datetime.now(timezone.utc),
            )
        )
        selection = create_selection(
            selection=schema.SelectionCreate(
                name="Player A wins",
                event_id=event.id,
                price=2.0,
                active=True,
                outcome="Unsettled",
            )
        )

    response = client.put(
        f"api/selections/{selection.id}",
        data=json.dumps(
            {"name": "Player B wins", "price": 2.5, "active": False, "outcome": "Win"}
        ),
        content_type="application/json",
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Player B wins"
    assert data["price"] == 2.5
    assert data["active"] is False
    assert data["outcome"] == "Win"


def test_update_nonexistent_selection(client):
    response = client.put(
        "api/selections/9999",
        data=json.dumps(
            {
                "name": "Nonexistent Selection",
                "price": 3.0,
                "active": False,
                "outcome": "Lose",
            }
        ),
        content_type="application/json",
    )
    assert response.status_code == 404


def test_get_selections(client):
    response = client.get("api/selections/")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


def test_get_selection_by_id(client):
    with client.application.app_context():
        sport = create_sport(
            sport=schema.SportCreate(name="Baseball", slug="baseball", active=True)
        )
        event = create_event(
            event=schema.EventCreate(
                name="Baseball Game",
                type="preplay",
                sport_id=sport.id,
                scheduled_start=datetime.now(timezone.utc),
            )
        )
        selection = create_selection(
            selection=schema.SelectionCreate(
                name="Team X wins",
                event_id=event.id,
                price=1.8,
                active=True,
                outcome="Unsettled",
            )
        )

    response = client.get(f"api/selections/{selection.id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Team X wins"
    assert data["price"] == 1.8


def test_get_selections_with_filters(client):
    with client.application.app_context():
        sport = create_sport(
            sport=schema.SportCreate(name="Soccer", slug="soccer", active=True)
        )
        event = create_event(
            event=schema.EventCreate(
                name="Soccer Match",
                type="preplay",
                sport_id=sport.id,
                scheduled_start=datetime.now(timezone.utc),
            )
        )
        create_selection(
            selection=schema.SelectionCreate(
                name="Team Y wins",
                event_id=event.id,
                price=1.9,
                active=True,
                outcome="Unsettled",
            )
        )

    response = client.get("api/selections/?price_gte=1.5&price_lte=2.0")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["price"] == 1.9


def test_selection_outcome_update(client):
    with client.application.app_context():
        sport = create_sport(
            sport=schema.SportCreate(name="Rugby", slug="rugby", active=True)
        )
        event = create_event(
            event=schema.EventCreate(
                name="Rugby Match",
                type="preplay",
                sport_id=sport.id,
                scheduled_start=datetime.now(timezone.utc),
            )
        )
        selection = create_selection(
            selection=schema.SelectionCreate(
                name="Team Z wins",
                event_id=event.id,
                price=2.2,
                active=True,
                outcome="Unsettled",
            )
        )

    # Update selection outcome to Win
    response = client.put(
        f"api/selections/{selection.id}",
        data=json.dumps({"outcome": "Win"}),
        content_type="application/json",
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["outcome"] == "Win"

    # Update selection outcome to Lose
    response = client.put(
        f"api/selections/{selection.id}",
        data=json.dumps({"outcome": "Lose"}),
        content_type="application/json",
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["outcome"] == "Lose"

    # Update selection outcome to Void
    response = client.put(
        f"api/selections/{selection.id}",
        data=json.dumps({"outcome": "Void"}),
        content_type="application/json",
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["outcome"] == "Void"

    # Update selection outcome to Unsettled
    response = client.put(
        f"api/selections/{selection.id}",
        data=json.dumps({"outcome": "Unsettled"}),
        content_type="application/json",
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["outcome"] == "Unsettled"


def test_event_inactive_when_all_selections_inactive(client):
    # Create a sport and an event
    with client.application.app_context():
        sport = create_sport(
            sport=schema.SportCreate(name="Soccer", slug="soccer", active=True)
        )
        event = create_event(
            event=schema.EventCreate(
                name="Soccer Match",
                type="preplay",
                sport_id=sport.id,
                scheduled_start=datetime.now(timezone.utc),
            )
        )

        # Create multiple selections for the event
        selection1 = create_selection(
            selection=schema.SelectionCreate(
                name="Team A wins",
                event_id=event.id,
                price=1.5,
                active=True,
                outcome="Unsettled",
            )
        )
        selection2 = create_selection(
            selection=schema.SelectionCreate(
                name="Team B wins",
                event_id=event.id,
                price=2.0,
                active=True,
                outcome="Unsettled",
            )
        )

    # Set all selections to inactive
    client.put(
        f"api/selections/{selection1.id}",
        data=json.dumps({"active": False}),
        content_type="application/json",
    )
    client.put(
        f"api/selections/{selection2.id}",
        data=json.dumps({"active": False}),
        content_type="application/json",
    )

    # Fetch the event to verify its status
    response = client.get(f"api/events/{event.id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["active"] is False


def test_invalid_selection_creation(client):
    response = client.post(
        "api/selections/",
        data=json.dumps(
            {
                "name": 99,
                "event_id": 1,
                "price": -1.0,
                "active": True,
                "outcome": "Invalid",
            }
        ),
        content_type="application/json",
    )
    assert response.status_code == 400


def test_create_selection_nonexistent_event(client):
    response = client.post(
        "api/selections/",
        data=json.dumps(
            {
                "name": "Invalid Selection",
                "event_id": 9999,
                "price": 1.5,
                "active": True,
                "outcome": "Unsettled",
            }
        ),
        content_type="application/json",
    )
    assert response.status_code == 404


def test_update_selection_invalid_data_types(client):
    with client.application.app_context():
        sport = create_sport(
            sport=schema.SportCreate(name="Tennis", slug="tennis", active=True)
        )
        event = create_event(
            event=schema.EventCreate(
                name="Tennis Match",
                type="preplay",
                sport_id=sport.id,
                scheduled_start=datetime.now(timezone.utc),
            )
        )
        selection = create_selection(
            selection=schema.SelectionCreate(
                name="Player A wins",
                event_id=event.id,
                price=2.0,
                active=True,
                outcome="Unsettled",
            )
        )

    response = client.put(
        f"api/selections/{selection.id}",
        data=json.dumps(
            {"name": 123, "price": "invalid", "active": "maybe", "outcome": 456}
        ),
        content_type="application/json",
    )
    assert response.status_code == 400


def test_get_selections_by_name_regex(client):
    with client.application.app_context():
        sport = create_sport(
            sport=schema.SportCreate(name="Soccer", slug="soccer", active=True)
        )
        event = create_event(
            event=schema.EventCreate(
                name="Soccer Match",
                type="preplay",
                sport_id=sport.id,
                scheduled_start=datetime.now(timezone.utc),
            )
        )
        create_selection(
            selection=schema.SelectionCreate(
                name="Winning Team",
                event_id=event.id,
                price=1.8,
                active=True,
                outcome="Unsettled",
            )
        )

    response = client.get("api/selections/?name_regex=Winning")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["name"] == "Winning Team"


def test_get_selections_by_complex_name_regex(client):
    with client.application.app_context():
        sport = create_sport(
            sport=schema.SportCreate(name="Soccer", slug="soccer", active=True)
        )
        event = create_event(
            event=schema.EventCreate(
                name="Soccer Match",
                type="preplay",
                sport_id=sport.id,
                scheduled_start=datetime.now(timezone.utc),
            )
        )
        create_selection(
            selection=schema.SelectionCreate(
                name="Team A wins",
                event_id=event.id,
                price=1.8,
                active=True,
                outcome="Unsettled",
            )
        )
        create_selection(
            selection=schema.SelectionCreate(
                name="Team B wins",
                event_id=event.id,
                price=2.0,
                active=True,
                outcome="Unsettled",
            )
        )
        create_selection(
            selection=schema.SelectionCreate(
                name="Team C scores",
                event_id=event.id,
                price=2.5,
                active=True,
                outcome="Unsettled",
            )
        )

    response = client.get("api/selections/?name_regex=Team [AB] wins")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "Team A wins"
    assert data[1]["name"] == "Team B wins"

    response = client.get("api/selections/?name_regex=Team\\s[C]\\s.*")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Team C scores"
