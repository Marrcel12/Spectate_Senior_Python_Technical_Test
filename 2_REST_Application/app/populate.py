from datetime import datetime, timedelta, timezone

from database import create_new_db, managed_cursor
from utils import slugify


def populate():
    with create_new_db() as conn:
        with managed_cursor(conn=conn) as cursor:

            # Populate sports
            sports = [
                ("Football", slugify("Football"), True),
                ("Basketball", slugify("Basketball"), True),
                ("Tennis", slugify("Tennis"), True),
                ("Baseball", slugify("Baseball"), True),
                ("Hockey", slugify("Hockey"), True),
                ("Inactive Sport 1", slugify("Inactive Sport 1"), False),
                ("Inactive Sport 2", slugify("Inactive Sport 2"), False),
            ]
            cursor.executemany(
                """INSERT INTO sports (name, slug, active) VALUES (?, ?, ?)""", sports
            )
            conn.commit()

            # Get sport IDs
            cursor.execute("""SELECT id, slug FROM sports""")
            sport_ids = {row[1]: row[0] for row in cursor.fetchall()}

            # Populate events
            events = [
                (
                    "Football Match 1",
                    slugify("Football Match 1"),
                    True,
                    "preplay",
                    sport_ids["football"],
                    "Pending",
                    datetime.now(timezone.utc),
                    None,
                ),
                (
                    "Football Match 2",
                    slugify("Football Match 2"),
                    True,
                    "preplay",
                    sport_ids["football"],
                    "Pending",
                    datetime.now(timezone.utc) + timedelta(days=2),
                    None,
                ),
                (
                    "Basketball Game 1",
                    slugify("Basketball Game 1"),
                    True,
                    "inplay",
                    sport_ids["basketball"],
                    "Started",
                    datetime.now(timezone.utc) - timedelta(hours=1),
                    datetime.now(timezone.utc) - timedelta(hours=1),
                ),
                (
                    "Basketball Game 2",
                    slugify("Basketball Game 2"),
                    True,
                    "preplay",
                    sport_ids["basketball"],
                    "Pending",
                    datetime.now(timezone.utc) + timedelta(days=3),
                    None,
                ),
                (
                    "Tennis Match 1",
                    slugify("Tennis Match 1"),
                    True,
                    "preplay",
                    sport_ids["tennis"],
                    "Pending",
                    datetime.now(timezone.utc) + timedelta(days=1),
                    None,
                ),
                (
                    "Baseball Game 1",
                    slugify("Baseball Game 1"),
                    True,
                    "preplay",
                    sport_ids["baseball"],
                    "Pending",
                    datetime.now(timezone.utc) + timedelta(days=4),
                    None,
                ),
                (
                    "Hockey Match 1",
                    slugify("Hockey Match 1"),
                    True,
                    "preplay",
                    sport_ids["hockey"],
                    "Pending",
                    datetime.now(timezone.utc) + timedelta(days=5),
                    None,
                ),
            ]
            cursor.executemany(
                """INSERT INTO events (name, slug, active, type, sport_id, status, scheduled_start, actual_start)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                events,
            )
            conn.commit()

            # Get event IDs
            cursor.execute("""SELECT id, slug FROM events""")
            event_ids = {row[1]: row[0] for row in cursor.fetchall()}

            # Populate selections
            selections = [
                # Football Match 1
                (
                    "Team A to Win",
                    event_ids["football-match-1"],
                    1.50,
                    True,
                    "Unsettled",
                ),
                ("Team B to Win", event_ids["football-match-1"], 2.75, True, "Lose"),
                ("Draw", event_ids["football-match-1"], 3.25, True, "Unsettled"),
                # Football Match 2
                ("Team C to Win", event_ids["football-match-2"], 1.60, True, "Win"),
                (
                    "Team D to Win",
                    event_ids["football-match-2"],
                    2.50,
                    True,
                    "Unsettled",
                ),
                ("Draw", event_ids["football-match-2"], 3.00, True, "Unsettled"),
                # Basketball Game 1
                (
                    "Player A to Score",
                    event_ids["basketball-game-1"],
                    1.80,
                    True,
                    "Void",
                ),
                (
                    "Player B to Score",
                    event_ids["basketball-game-1"],
                    2.25,
                    True,
                    "Unsettled",
                ),
                # Basketball Game 2
                (
                    "Player C to Score",
                    event_ids["basketball-game-2"],
                    1.90,
                    True,
                    "Unsettled",
                ),
                (
                    "Player D to Score",
                    event_ids["basketball-game-2"],
                    2.15,
                    True,
                    "Unsettled",
                ),
                # Tennis Match 1
                ("Player X to Win", event_ids["tennis-match-1"], 1.90, True, "Lose"),
                (
                    "Player Y to Win",
                    event_ids["tennis-match-1"],
                    2.10,
                    True,
                    "Unsettled",
                ),
                # Baseball Game 1
                ("Team E to Win", event_ids["baseball-game-1"], 1.70, True, "Void"),
                (
                    "Team F to Win",
                    event_ids["baseball-game-1"],
                    2.40,
                    True,
                    "Unsettled",
                ),
                # Hockey Match 1
                ("Team G to Win", event_ids["hockey-match-1"], 1.55, True, "Unsettled"),
                ("Team H to Win", event_ids["hockey-match-1"], 2.60, True, "Win"),
                ("Draw", event_ids["hockey-match-1"], 3.50, True, "Unsettled"),
            ]
            cursor.executemany(
                """INSERT INTO selections (name, event_id, price, active, outcome) VALUES (?, ?, ?, ?, ?)""",
                selections,
            )
            conn.commit()


if __name__ == "__main__":
    populate()
    print("Database populated with initial data.")
