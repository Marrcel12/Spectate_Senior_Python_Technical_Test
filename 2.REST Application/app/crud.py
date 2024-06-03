import sqlite3
from typing import List, Optional

from .exceptions import DuplicateValueError
from . import schemas, utils

DATABASE_URL = "test.db"


def get_connection():
    conn = sqlite3.connect(DATABASE_URL)
    return conn


def create_sport(sport: schemas.SportCreate) -> schemas.Sport:
    conn = get_connection()
    cursor = conn.cursor()
    slug = utils.slugify(value=sport.name)
    if cursor.execute("""SELECT id FROM sports WHERE slug = ?""", (slug,)).fetchone():
        raise DuplicateValueError(value=sport.name, collection="sports")
    cursor.execute(
        """INSERT INTO sports (name, slug, active)
                      VALUES (?, ?, ?)""",
        (sport.name, slug, True),
    )
    conn.commit()
    sport_id = cursor.lastrowid
    conn.close()
    return schemas.Sport(id=sport_id, name=sport.name, slug=slug, active=True)


def update_sport(sport_id: int, sport: schemas.SportUpdate) -> schemas.Sport:
    conn = get_connection()
    cursor = conn.cursor()
    current_sport = get_sport(sport_id)

    name = sport.name if sport.name is not None else current_sport.name
    slug = utils.slugify(name)

    active = sport.active if sport.active is not None else current_sport.active

    cursor.execute(
        """UPDATE sports SET name = ?, slug = ?, active = ? WHERE id = ?""",
        (name, slug, active, sport_id),
    )
    conn.commit()
    conn.close()
    return get_sport(sport_id)


def get_sport(sport_id: int) -> schemas.Sport:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT id, name, slug, active FROM sports WHERE id = ?""", (sport_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return schemas.Sport(id=row[0], name=row[1], slug=row[2], active=row[3])


def get_sports(filters: Optional[dict] = None) -> List[schemas.Sport]:
    conn = get_connection()
    cursor = conn.cursor()

    query = """SELECT id, name, slug, active FROM sports WHERE 1=1"""
    params = []
    if filters:
        for key, value in filters.items():
            if key == "name_like":
                query += " AND name LIKE ?"
                params.append(f"%{value}%")
            else:
                query += f" AND {key}=?"
                params.append(utils.bool_string_to_int(value))
                
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [
        schemas.Sport(id=row[0], name=row[1], slug=row[2], active=row[3])
        for row in rows
    ]


def create_event(event: schemas.EventCreate) -> schemas.Event:
    conn = get_connection()
    cursor = conn.cursor()
    slug = utils.slugify(event.name)
    if cursor.execute("""SELECT id FROM events WHERE slug = ?""", (slug,)).fetchone():
        raise DuplicateValueError(value=event.name, collection="events")
    cursor.execute(
        """INSERT INTO events (name, slug, active, type, sport_id, status, scheduled_start)
                      VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            event.name,
            slug,
            True,
            event.type,
            event.sport_id,
            "Pending",
            event.scheduled_start,
        ),
    )
    conn.commit()
    event_id = cursor.lastrowid
    conn.close()
    return schemas.Event(
        id=event_id,
        name=event.name,
        slug=slug,
        active=True,
        type=event.type,
        sport_id=event.sport_id,
        status="Pending",
        scheduled_start=event.scheduled_start,
        actual_start=None,
    )


def update_event(event_id: int, event: schemas.EventUpdate) -> schemas.Event:
    conn = get_connection()
    cursor = conn.cursor()
    current_event = get_event(event_id)

    name = event.name if event.name is not None else current_event.name
    slug = utils.slugify(name)

    active = event.active if event.active is not None else current_event.active
    status = event.status if event.status is not None else current_event.status

    cursor.execute(
        """UPDATE events SET name = ?, slug = ?, active = ?, status = ? WHERE id = ?""",
        (name, slug, active, status, event_id),
    )
    conn.commit()

    if status == "Started":
        cursor.execute(
            """UPDATE events SET actual_start = datetime('now') WHERE id = ?""",
            (event_id,),
        )
        conn.commit()

    conn.close()
    return get_event(event_id)


def get_event(event_id: int) -> schemas.Event:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT id, name, slug, active, type, sport_id, status, scheduled_start, actual_start
                      FROM events WHERE id = ?""",
        (event_id,),
    )
    row = cursor.fetchone()
    conn.close()
    return schemas.Event(
        id=row[0],
        name=row[1],
        slug=row[2],
        active=row[3],
        type=row[4],
        sport_id=row[5],
        status=row[6],
        scheduled_start=row[7],
        actual_start=row[8],
    )


def get_events(filters: Optional[dict] = None) -> List[schemas.Event]:
    conn = get_connection()
    cursor = conn.cursor()

    query = """SELECT id, name, slug, active, type, sport_id, status, scheduled_start, actual_start FROM events WHERE 1=1"""
    params = []
    if filters:
        for key, value in filters.items():
            print(key, value)
            if key == "scheduled_start_gte":
                query += " AND scheduled_start >= ?"
                params.append(value)
            elif  key == "scheduled_start_lte":
                query += " AND scheduled_start <= ?"
                params.append(value)
            elif key == "name_like":
                query += " AND name LIKE ?"
                params.append(f"%{value}%")
            else:
                query += f" AND {key}=?"
                params.append(utils.bool_string_to_int(value))
    print(query, params)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [
        schemas.Event(
            id=row[0],
            name=row[1],
            slug=row[2],
            active=row[3],
            type=row[4],
            sport_id=row[5],
            status=row[6],
            scheduled_start=row[7],
            actual_start=row[8],
        )
        for row in rows
    ]


def create_selection(selection: schemas.SelectionCreate) -> schemas.Selection:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO selections (name, event_id, price, active, outcome)
                      VALUES (?, ?, ?, ?, ?)""",
        (selection.name, selection.event_id, selection.price, True, "Unsettled"),
    )
    conn.commit()
    selection_id = cursor.lastrowid
    conn.close()
    return schemas.Selection(
        id=selection_id,
        name=selection.name,
        event_id=selection.event_id,
        price=selection.price,
        active=True,
        outcome="Unsettled",
    )


def update_selection(
    selection_id: int, selection: schemas.SelectionUpdate
) -> schemas.Selection:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE selections SET name = ?, active = ?, outcome = ? WHERE id = ?""",
        (selection.name, selection.active, selection.outcome, selection_id),
    )
    conn.commit()
    conn.close()

    # If all selections of the event are inactive, make the event inactive
    cursor.execute(
        """UPDATE events SET active = (SELECT CASE WHEN COUNT(*) = 0 THEN 0 ELSE 1 END
                      FROM selections WHERE event_id = ? AND active = 1) WHERE id = ?""",
        (selection.event_id, selection.event_id),
    )
    conn.commit()

    # If all events of the sport are inactive, make the sport inactive
    cursor.execute(
        """UPDATE sports SET active = (SELECT CASE WHEN COUNT(*) = 0 THEN 0 ELSE 1 END
                      FROM events WHERE sport_id = ? AND active = 1) WHERE id = (SELECT sport_id FROM events WHERE id = ?)""",
        (selection.event_id, selection.event_id),
    )
    conn.commit()

    return get_selection(selection_id)


def get_selection(selection_id: int) -> schemas.Selection:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT id, name, event_id, price, active, outcome FROM selections WHERE id = ?""",
        (selection_id,),
    )
    row = cursor.fetchone()
    conn.close()
    return schemas.Selection(
        id=row[0],
        name=row[1],
        event_id=row[2],
        price=row[3],
        active=row[4],
        outcome=row[5],
    )


def get_selections(filters: Optional[dict] = None) -> List[schemas.Selection]:
    conn = get_connection()
    cursor = conn.cursor()

    query = """SELECT id, name, event_id, price, active, outcome FROM selections WHERE 1=1"""
    params = []
    if filters:
        for key, value in filters.items():
            if key == "price_gte" in filters:
                query += " AND price >= ?"
                params.append(value)
            elif key == "price_lte" in filters:
                query += " AND price <= ?"
                params.append(value)
            elif key == "name_like":
                query += " AND name LIKE ?"
                params.append(f"%{value}%")
            else:
                query += f" AND {key}=?"
                params.append(utils.bool_string_to_int(value))

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [
        schemas.Selection(
            id=row[0],
            name=row[1],
            event_id=row[2],
            price=row[3],
            active=row[4],
            outcome=row[5],
        )
        for row in rows
    ]
