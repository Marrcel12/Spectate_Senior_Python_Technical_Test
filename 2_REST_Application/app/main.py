from typing import Literal

from flask import Blueprint, current_app, jsonify, request
from flask.wrappers import Response
from pydantic import ValidationError

from . import crud, schemas
from .exceptions import DuplicateValueError, NotExistError

main_bp = Blueprint("main", __name__)


def handle_errors(f):
    """
    Decorator function that handles DuplicateValueError exceptions raised by the decorated function.

    Parameters:
    - f (function): The function to be decorated.

    Returns:
    - decorated_function (function): The decorated function that handles DuplicateValueError exceptions.

    Raises:
    - DuplicateValueError: If a duplicate value is found in the collection.
    - ValidationError: If a ValidationError is raised by the decorated function.

    The decorated function attempts to execute the original function. If a any given error is raised,
    it creates a JSON response with an error message indicating the error. The
    response status code is set to 400. The decorated function then returns the JSON response.
    """

    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except DuplicateValueError as e:
            return (
                jsonify(
                    {
                        "error": "DuplicateValueError",
                        "message": f'Duplicate value "{e.value}" found in collection "{e.collection}".',
                    }
                ),
                400,
            )
        except ValidationError as e:
            return jsonify({"error": "ValidationError", "message": str(e)}), 400
        except NotExistError as e:
            return jsonify({"error": "NotExistError", "message": str(e)}), 404

    decorated_function.__name__ = f.__name__
    return decorated_function


# sports endpoints
@main_bp.route("/sports/", methods=["POST"])
@handle_errors
def create_sport():
    sport_data = request.json
    sport = schemas.SportCreate(**sport_data)
    new_sport = crud.create_sport(sport)
    return jsonify(new_sport.model_dump()), 201


@main_bp.route("/sports/<int:sport_id>", methods=["PUT"])
@handle_errors
def update_sport(sport_id):
    sport_data = request.json
    sport = schemas.SportUpdate(**sport_data)
    updated_sport = crud.update_sport(sport_id, sport)
    return jsonify(updated_sport.model_dump()), 200


@main_bp.route("/sports/", methods=["GET"])
def read_sports():
    filters = request.args.to_dict()
    sports = crud.get_sports(filters)
    return jsonify([sport.model_dump() for sport in sports]), 200


@main_bp.route("/sports/<int:sport_id>", methods=["GET"])
@handle_errors
def read_sport(sport_id):
    sport = crud.get_sport(sport_id)
    return jsonify(sport.model_dump()), 200


# Events endpoints
@main_bp.route("/events/", methods=["POST"])
@handle_errors
def create_event():
    event_data = request.json
    event = schemas.EventCreate(**event_data)
    new_event = crud.create_event(event)
    return jsonify(new_event.model_dump()), 201


@main_bp.route("/events/<int:event_id>", methods=["PUT"])
@handle_errors
def update_event(event_id):
    event_data = request.json
    event = schemas.EventUpdate(**event_data)
    updated_event = crud.update_event(event_id, event)
    return jsonify(updated_event.model_dump()), 200


@main_bp.route("/events/", methods=["GET"])
def read_events() -> tuple[Response, Literal[200]]:
    filters = request.args.to_dict()
    events = crud.get_events(filters)
    return jsonify([event.model_dump() for event in events]), 200


@main_bp.route("/events/<int:event_id>", methods=["GET"])
@handle_errors
def read_event(event_id):
    event = crud.get_event(event_id)
    return jsonify(event.model_dump()), 200


# Selections endpoints
@main_bp.route("/selections/", methods=["POST"])
@handle_errors
def create_selection():
    selection_data = request.json
    selection = schemas.SelectionCreate(**selection_data)
    new_selection = crud.create_selection(selection)
    return jsonify(new_selection.model_dump()), 201


@main_bp.route("/selections/<int:selection_id>", methods=["PUT"])
@handle_errors
def update_selection(selection_id):
    selection_data = request.json
    selection = schemas.SelectionUpdate(**selection_data)
    updated_selection = crud.update_selection(selection_id, selection)
    return jsonify(updated_selection.model_dump()), 200


@main_bp.route("/selections/", methods=["GET"])
def read_selections():
    filters = request.args.to_dict()
    selections = crud.get_selections(filters)
    return jsonify([selection.model_dump() for selection in selections]), 200


@main_bp.route("/selections/<int:selection_id>", methods=["GET"])
@handle_errors
def read_selection(selection_id):
    selection = crud.get_selection(selection_id)
    return jsonify(selection.model_dump()), 200
