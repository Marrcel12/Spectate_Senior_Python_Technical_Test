from typing import List, Optional

from flask import current_app

from . import schemas, utils
from .database import get_connection, managed_cursor
from .exceptions import DuplicateValueError, NotExistError


def create_sport(sport: schemas.SportCreate) -> schemas.Sport:
    conn = get_connection(current_app.config["conn_url"])
    with managed_cursor(conn) as cursor:
        slug = utils.slugify(value=sport.name)
        if cursor.execute(
            """SELECT id FROM sports WHERE slug = ?""", (slug,)
        ).fetchone():
            raise DuplicateValueError(value=sport.name, collection="sports")
        cursor.execute(
            """INSERT INTO sports (name, slug, active)
                        VALUES (?, ?, ?)""",
            (sport.name, slug, True),
        )
        conn.commit()
        sport_id = cursor.lastrowid
        return schemas.Sport(id=sport_id, name=sport.name, slug=slug, active=True)


def update_sport(sport_id: int, sport: schemas.SportUpdate) -> schemas.Sport:
    conn = get_connection(current_app.config["conn_url"])
    with managed_cursor(conn) as cursor:
        current_sport = get_sport(sport_id)

        name = sport.name if sport.name is not None else current_sport.name
        slug = utils.slugify(name)

        active = sport.active if sport.active is not None else current_sport.active

        cursor.execute(
            """UPDATE sports SET name = ?, slug = ?, active = ? WHERE id = ?""",
            (name, slug, active, sport_id),
        )
        conn.commit()
        return get_sport(sport_id)


def get_sport(sport_id: int) -> schemas.Sport:
    conn = get_connection(current_app.config["conn_url"])
    with managed_cursor(conn) as cursor:
        cursor.execute(
            """SELECT id, name, slug, active FROM sports WHERE id = ?""",
            (sport_id,),
        )
        if row := cursor.fetchone():
            return schemas.Sport(id=row[0], name=row[1], slug=row[2], active=row[3])
        raise NotExistError(value=sport_id, collection="sports")


def get_sports(filters: Optional[dict] = None) -> List[schemas.Sport]:
    conn = get_connection(current_app.config["conn_url"])
    with managed_cursor(conn) as cursor:

        query = """SELECT id, name, slug, active FROM sports WHERE 1=1"""
        params = []
        if filters:
            for key, value in filters.items():
                if key == "name_regex":
                    query += " AND name REGEXP ?"
                    params.append(value)
                elif key == "min_active_events":
                    query += """ AND id IN (SELECT sport_id FROM events WHERE active=1 GROUP BY sport_id HAVING COUNT(*) >= ?)"""
                    params.append(int(value))
                else:
                    query += f" AND {key}=?"
                    params.append(utils.bool_string_to_int(value))
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [
            schemas.Sport(id=row[0], name=row[1], slug=row[2], active=row[3])
            for row in rows
        ]


def create_event(event: schemas.EventCreate) -> schemas.Event:
    conn = get_connection(current_app.config["conn_url"])
    with managed_cursor(conn) as cursor:
        slug = utils.slugify(event.name)
        if cursor.execute(
            """SELECT id FROM events WHERE slug = ?""", (slug,)
        ).fetchone():
            raise DuplicateValueError(value=event.name, collection="events")
        if (
            cursor.execute(
                """SELECT id FROM sports WHERE id = ?""", (event.sport_id,)
            ).fetchone()
            is None
        ):
            raise NotExistError(value=event.sport_id, collection="sports")
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
    conn = get_connection(current_app.config["conn_url"])
    with managed_cursor(conn) as cursor:
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
        # Check if all events for the sport are inactive

        cursor.execute(
            """UPDATE sports SET active = (SELECT CASE WHEN COUNT(*) = 0 THEN 0 ELSE 1 END
                            FROM events WHERE sport_id = ? AND active = 1)
                            WHERE id = (SELECT sport_id FROM events WHERE id = ?)""",
            (current_event.sport_id, event_id),
        )
        conn.commit()

        return get_event(event_id)


def get_event(event_id: int) -> schemas.Event:
    conn = get_connection(current_app.config["conn_url"])
    with managed_cursor(conn) as cursor:
        cursor.execute(
            """SELECT id, name, slug, active, type, sport_id, status, scheduled_start, actual_start
                            FROM events WHERE id = ?""",
            (event_id,),
        )
        if row := cursor.fetchone():
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
        raise NotExistError(value=event_id, collection="events")


def get_events(filters: Optional[dict] = None) -> List[schemas.Event]:
    conn = get_connection(current_app.config["conn_url"])
    with managed_cursor(conn) as cursor:

        query = """SELECT id, name, slug, active, type, sport_id, status, scheduled_start, actual_start FROM events WHERE 1=1"""
        params = []
        if filters:
            for key, value in filters.items():
                if key == "scheduled_start_gte":
                    query += " AND scheduled_start >= ?"
                    params.append(value)
                elif key == "scheduled_start_lte":
                    query += " AND scheduled_start <= ?"
                    params.append(value)
                elif key == "name_regex":
                    query += " AND name REGEXP ?"
                    params.append(value)
                elif key == "min_active_selections":
                    query += """ AND id IN (SELECT event_id FROM selections WHERE active=1 GROUP BY event_id HAVING COUNT(*) >= ?)"""
                    params.append(value)
                else:
                    query += f" AND {key}=?"
                    params.append(utils.bool_string_to_int(value))
        cursor.execute(query, params)
        rows = cursor.fetchall()
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
    conn = get_connection(current_app.config["conn_url"])
    with managed_cursor(conn) as cursor:
        if (
            cursor.execute(
                """Select 1 from events where id = ?""", (selection.event_id,)
            ).fetchone()
            is None
        ):
            raise NotExistError(value=selection.event_id, collection="events")
        cursor.execute(
            """INSERT INTO selections (name, event_id, price, active, outcome)
                            VALUES (?, ?, ?, ?, ?)""",
            (
                selection.name,
                selection.event_id,
                selection.price,
                True,
                "Unsettled",
            ),
        )
        conn.commit()
        selection_id = cursor.lastrowid
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
    conn = get_connection(current_app.config["conn_url"])
    with managed_cursor(conn) as cursor:

        # Fetch the current selection to get its event_id
        current_selection = get_selection(selection_id)
        event_id = current_selection.event_id

        # Update the selection with the provided data
        cursor.execute(
            """UPDATE selections SET name = ?, active = ?, outcome = ?, price = ? WHERE id = ?""",
            (
                (
                    selection.name
                    if selection.name is not None
                    else current_selection.name
                ),
                (
                    selection.active
                    if selection.active is not None
                    else current_selection.active
                ),
                (
                    selection.outcome
                    if selection.outcome is not None
                    else current_selection.outcome
                ),
                (
                    selection.price
                    if selection.price is not None
                    else current_selection.price
                ),
                selection_id,
            ),
        )
        conn.commit()

        # If all selections of the event are inactive, make the event inactive
        cursor.execute(
            """UPDATE events SET active = (SELECT CASE WHEN COUNT(*) = 0 THEN 0 ELSE 1 END
                            FROM selections WHERE event_id = ? AND active = 1) WHERE id = ?""",
            (event_id, event_id),
        )
        conn.commit()

        # If all events of the sport are inactive, make the sport inactive
        cursor.execute(
            """UPDATE sports SET active = (SELECT CASE WHEN COUNT(*) = 0 THEN 0 ELSE 1 END
                            FROM events WHERE sport_id = ? AND active = 1) WHERE id = (SELECT sport_id FROM events WHERE id = ?)""",
            (event_id, event_id),
        )
        conn.commit()

        return get_selection(selection_id)


def get_selection(selection_id: int) -> schemas.Selection:
    conn = get_connection(current_app.config["conn_url"])
    with managed_cursor(conn) as cursor:
        cursor.execute(
            """SELECT id, name, event_id, price, active, outcome FROM selections WHERE id = ?""",
            (selection_id,),
        )
        if row := cursor.fetchone():
            return schemas.Selection(
                id=row[0],
                name=row[1],
                event_id=row[2],
                price=row[3],
                active=row[4],
                outcome=row[5],
            )
        raise NotExistError(value=selection_id, collection="selections")


def get_selections(filters: Optional[dict] = None) -> List[schemas.Selection]:
    conn = get_connection(current_app.config["conn_url"])
    with managed_cursor(conn) as cursor:

        query = """SELECT id, name, event_id, price, active, outcome FROM selections WHERE 1=1"""
        params = []
        if filters:
            for key, value in filters.items():
                if key == "price_gte":
                    query += " AND price >= ?"
                    params.append(value)
                elif key == "price_lte":
                    query += " AND price <= ?"
                    params.append(value)
                elif key == "name_regex":
                    query += " AND name REGEXP ?"
                    params.append(value)
                else:
                    query += f" AND {key}=?"
                    params.append(utils.bool_string_to_int(value))
        cursor.execute(query, params)
        rows = cursor.fetchall()
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
