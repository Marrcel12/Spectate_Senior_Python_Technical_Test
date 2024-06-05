import pytest
from app import create_app
from app.database import create_new_db, delete_db

NAME_OF_TEST_DB = "test.db"


@pytest.fixture
def client():
    app = create_app(NAME_OF_TEST_DB)
    app.config["TESTING"] = True
    with create_new_db(NAME_OF_TEST_DB) as conn:
        with app.test_client() as client:
            yield client
