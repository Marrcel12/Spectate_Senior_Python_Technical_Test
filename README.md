# Spectate_Senior_Python_Technical_Test

## Project 1 Overview

This project implements a solution to calculate the number of internal nodes in a tree represented as a list. An internal node is any node of a tree that has at least one child. The setup utilizes Docker and Docker Compose for easy configuration and execution.

## Project Structure

- `Dockerfile`: Defines the Docker image configuration.
- `docker-compose.yml`: Defines the services and configurations for Docker Compose.
- `tree.py`: The Python script that calculates the number of internal nodes in a tree.


## Setup and Run

### 1. Build the Docker image

```sh
docker-compose build
```

### 2. Run the Python script interactively

```sh
docker-compose run python-app
```

## Example Usage

When you run the command `docker-compose run python-app`, you will be prompted to enter the tree structure as a list of integers separated by spaces.

```sh
Enter the tree structure as a list of integers separated by spaces: -1 0 1 1 1 2 2 2 3 3 3 4 4 4
Number of internal nodes: 5
```

## Explanation

- **Dockerfile**: Sets up the Python environment, installs dependencies, and specifies the default command to keep the container running interactively.
- **docker-compose.yml**: Configures the service to run interactively with stdin open and a pseudo-TTY allocated.
- **tree.py**: Python script that reads input, processes it, and prints the result.

---

## Logic Overview

### Tree Structure Analysis

The function `find_internal_nodes_num` calculates the number of internal nodes in a tree. The tree is represented as a list where each index corresponds to a node, and the value at each index represents the parent node. The root node is denoted by -1. The function identifies unique parent nodes using a set and counts them, excluding the root node.

Here is the implementation of the function:

```python
def find_internal_nodes_num(L):
    """
    Calculate the number of internal nodes in a tree represented as a list.

    Args:
        L (List[int]): A list representing the tree structure. Each element in the list
            represents a node in the tree. The root node is represented by -1.

    Returns:
        int: The number of internal nodes in the tree.
    """
    return len(set((L)))-1

if __name__ == "__main__":
    input_list = list(map(int, input("Enter the tree structure as a list of integers separated by spaces: ").split()))
    result = find_internal_nodes_num(input_list)
    print(f"Number of internal nodes: {result}")
```

This function is designed to efficiently handle large trees by leveraging set operations to quickly count unique parent nodes.

---

## Setup Instructions

---

This project sets up a Docker environment to run a Python script that calculates the number of internal nodes in a tree represented as a list. 
The setup uses Docker Compose for easy configuration and execution.

## Project Structure

- `Dockerfile`: Defines the Docker image configuration.
- `docker-compose.yml`: Defines the services and configurations for Docker Compose.
- `tree.py`: The Python script that calculates the number of internal nodes in a tree.
- `requirements.txt`: A file for specifying Python dependencies (empty if no external dependencies are required).

## Prerequisites

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Setup and Run

### 1. Build the Docker image

```sh
docker-compose build
```

### 2. Run the Python script interactively

```sh
docker-compose run python-app python tree.py
```

## Example Usage

When you run the command `docker-compose run python-app python tree.py`, you will be prompted to enter the tree structure as a list of integers separated by spaces.

```sh
Enter the tree structure as a list of integers separated by spaces: -1 0 1 1 1 2 2 2 3 3 3 4 4 4
Number of internal nodes: 5
```

## Explanation

- **Dockerfile**: Sets up the Python environment, installs dependencies, and specifies the default command to keep the container running interactively.
- **docker-compose.yml**: Configures the service to run interactively with stdin open and a pseudo-TTY allocated.
- **tree.py**: Python script that reads input, processes it, and prints the result.

---


# Project 2 Overview

This project is a simple REST API for managing sports, events, and selections. It is designed to handle creation, updating, and searching for these entities. The API is built using Flask and follows a structured approach for handling requests, validations, and errors. The project also includes database management using SQLite with migrations handled by Alembic.

## Features

- **CRUD Operations**: Create, Read, Update, Delete operations for sports, events, and selections.
- **Filtering**: Search functionality with multiple filters combined using AND expressions.
- **Error Handling**: Custom error handling for various exceptions.
- **Database Management**: SQLite database management with Alembic for migrations.
- **Containerization**: Docker and Docker Compose configurations for easy setup and deployment.
- **Unit Testing**: Unit tests to ensure functionality and reliability.

## System Requirements

- **Python**: Implemented using Python.
- **Web Framework**: Flask.
- **Database**: SQLite (raw SQL queries, no ORM).
- **Containerization**: Docker and Docker Compose.
- **Testing**: Unit tests included.

## Setup Instructions

### Prerequisites

- Python
- Docker
- Docker Compose

### Installation

1. **Create a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

2. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Run the database migrations**:
    ```sh
    alembic upgrade head
    ```

4. **Run the application**:
    ```sh
    flask run
    ```

### Docker

1. **Build and run the Docker container**:
    ```sh
    docker-compose up --build
    ```

This will set up the application and its dependencies in a Docker container.

## API Endpoints
All endpoints are aviable under /api

### Sports
- **Create Sport**:
    ```sh
    POST /sports/
    ```
- **Update Sport**:
    ```sh
    PUT /sports/<int:sport_id>
    ```
- **Get Sports**:
    ```sh
    GET /sports/
    ```
- **Get Sport by ID**:
    ```sh
    GET /sports/<int:sport_id>
    ```

### Events

- **Create Event**:
    ```sh
    POST /events/
    ```
- **Update Event**:
    ```sh
    PUT /events/<int:event_id>
    ```
- **Get Events**:
    ```sh
    GET /events/
    ```
- **Get Event by ID**:
    ```sh
    GET /events/<int:event_id>
    ```

### Selections

- **Create Selection**:
    ```sh
    POST /selections/
    ```
- **Update Selection**:
    ```sh
    PUT /selections/<int:selection_id>
    ```
- **Get Selections**:
    ```sh
    GET /selections/
    ```
- **Get Selection by ID**:
    ```sh
    GET /selections/<int:selection_id>
    ```

## Error Handling

The application has a custom error handler that manages the following exceptions:

- `DuplicateValueError`
- `ValidationError`
- `NotExistError`

These errors will return appropriate JSON responses with the error message and status code.

## Database Management

The database operations are managed using SQLite. Migrations are handled using Alembic to ensure the database schema stays up-to-date with the application's models.

### Database Connection

The database connection is managed through a context manager that ensures the connection is properly closed after operations. Regular expressions can be used in queries through a custom SQLite function.

### Migrations

Migrations are applied using Alembic. Configuration for Alembic is provided in `alembic.ini`, and the database URL is dynamically set in the code.

## Testing

Unit tests are provided to ensure the functionality of the API. To run the tests, use:

```sh
pytest
```

# Unit Test Coverage for REST API

This part of document outlines the unit tests for the REST API that manages sports, events, and selections. The tests are designed to cover all the cases specified in the project requirements(PDF).

### Test Files

- `test_sports.py`
- `test_events.py`
- `test_selections.py`

### Overview

The REST API includes the following functionalities for managing sports, events, and selections:
1. Creating sports, events, or selections.
2. Updating sports, events, or selections.
3. Searching for sports, events, or selections with various filters.
4. Business logic to handle the state changes in sports and events based on the activity of their related entities (events and selections respectively).

### Test Cases Coverage

#### Sports Management (`test_sports.py`)

1. **Creating a Sport:**
   - **Valid data:** Tests creating a sport with valid name, slug, and active status.
   - **Duplicate names or slugs:** Tests creating a sport with a duplicate slug.
   - **Invalid data types:** Tests creating a sport with invalid data types.
   - **Missing required fields:** Tests creating a sport with missing required fields.

2. **Updating a Sport:**
   - **Valid data:** Tests updating an existing sport with valid data.
   - **Non-existent sport:** Tests updating a non-existent sport.
   - **Invalid data types:** Tests updating a sport with invalid data types.

3. **Searching for Sports:**
   - **Retrieve all sports:** Tests retrieving all sports.
   - **Retrieve by name regex:** Tests retrieving sports by name using regex (including complex regex).
   - **Retrieve by active status:** Tests retrieving sports by active status.
   - **Minimum number of active events:** Tests retrieving sports with a minimum number of active events.

4. **Business Logic:**
   - **Sport becomes inactive when all events are inactive:** Tests that a sport becomes inactive when all its events are inactive.

#### Events Management (`test_events.py`)

1. **Creating an Event:**
   - **Valid data:** Tests creating an event with valid name, type, sport, and scheduled start.
   - **Non-existent sport:** Tests creating an event with a non-existent sport.
   - **Missing required fields:** Tests creating an event with missing required fields.
   - **Invalid data types:** Tests creating an event with invalid data types.

2. **Updating an Event:**
   - **Valid data:** Tests updating an existing event with valid data.
   - **Non-existent event:** Tests updating a non-existent event.
   - **Invalid data types:** Tests updating an event with invalid data types.
   - **Status changed to "Started":** Tests updating the status of an event to "Started" and verifying the actual start time is set.

3. **Searching for Events:**
   - **Retrieve all events:** Tests retrieving all events.
   - **Retrieve by name regex:** Tests retrieving events by name using regex (including complex regex).
   - **Retrieve by active status:** Tests retrieving events by active status.
   - **Retrieve by type (preplay/inplay):** Tests retrieving events by type.
   - **Scheduled start in timeframe:** Tests retrieving events scheduled to start in a specific timeframe.

4. **Business Logic:**
   - **Event becomes inactive when all selections are inactive:** Tests that an event becomes inactive when all its selections are inactive.

#### Selections Management (`test_selections.py`)

1. **Creating a Selection:**
   - **Valid data:** Tests creating a selection with valid name, event, price, active status, and outcome.
   - **Non-existent event:** Tests creating a selection with a non-existent event.
   - **Missing required fields:** Tests creating a selection with missing required fields.
   - **Invalid data types:** Tests creating a selection with invalid data types.

2. **Updating a Selection:**
   - **Valid data:** Tests updating an existing selection with valid data.
   - **Non-existent selection:** Tests updating a non-existent selection.
   - **Invalid data types:** Tests updating a selection with invalid data types.
   - **Updating outcome:** Tests updating the outcome of a selection.

3. **Searching for Selections:**
   - **Retrieve all selections:** Tests retrieving all selections.
   - **Retrieve by name regex:** Tests retrieving selections by name using regex (including complex regex).
   - **Retrieve by active status:** Tests retrieving selections by active status.
   - **Retrieve by outcome:** Tests retrieving selections by outcome.

4. **Business Logic:**
   - **Event becomes inactive when all selections are inactive:** Tests that an event becomes inactive when all its selections are inactive.

### Notes

- Ensure that the testing environment is properly set up before running the tests.
- The tests assume that the database and application context are correctly configured.
- Running these tests will verify the functionality and robustness of the REST API.
---
## Running Unit Tests and Viewing Coverage Results

This document provides instructions on how to run the unit tests for the REST API and how to view the test coverage results. 

### Prerequisites

Ensure you have the following installed:
- Python 3.x
- `pip` (Python package installer)
- `pytest` and `pytest-cov` for running tests and generating coverage reports

### Setup Instructions

1. **Install Dependencies:**

   ```sh
   pip install -r requirements.txt
   ```


### Running the Unit Tests

To run the unit tests, execute the following command:

```sh
pytest --cov=app --cov-report=html --cov-report=term
```

### Viewing the Coverage Report

After running the tests, the coverage report will be generated in the `htmlcov` directory. You can open the `index.html` file in a web browser to view a detailed coverage report:

```sh
open htmlcov/index.html
```

### Coverage Summary

The coverage results are also available in JSON format. Here is an overview of the coverage based on the latest run:

- **Overall Coverage:** 97.3%
- **Total Statements:** 815
- **Covered Statements:** 793
- **Missing Statements:** 22

### Detailed Coverage Results

The following is a summary of the coverage for each file:

| File                                      | Statements | Covered | Missed | Coverage (%) |
|-------------------------------------------|------------|---------|--------|---------------|
| `alembic/env.py`                          | 24         | 19      | 5      | 79.17         |
| `alembic/versions/723870d04286_initial_migration.py` | 31         | 20      | 11     | 64.52         |
| `app/__init__.py`                         | 10         | 9       | 1      | 90.00         |
| `app/crud.py`                             | 158        | 153     | 5      | 96.84         |
| `app/database.py`                         | 34         | 34      | 0      | 100.00        |
| `app/exceptions.py`                       | 10         | 10      | 0      | 100.00        |
| `app/main.py`                             | 91         | 91      | 0      | 100.00        |
| `app/models.py`                           | 33         | 33      | 0      | 100.00        |
| `app/schemas.py`                          | 55         | 55      | 0      | 100.00        |
| `app/utils.py`                            | 11         | 11      | 0      | 100.00        |
| `tests/__init__.py`                       | 0          | 0       | 0      | 100.00        |
| `tests/conftest.py`                       | 11         | 11      | 0      | 100.00        |
| `tests/test_events.py`                    | 111        | 111     | 0      | 100.00        |
| `tests/test_selections.py`                | 133        | 133     | 0      | 100.00        |
| `tests/test_sports.py`                    | 103        | 103     | 0      | 100.00        |

### Running Individual Test Files

To run tests from specific files, you can use the following commands:

- **For Sports:**

  ```sh
  pytest tests/test_sports.py --cov=app --cov-report=html --cov-report=term
  ```

- **For Events:**

  ```sh
  pytest tests/test_events.py --cov=app --cov-report=html --cov-report=term
  ```

- **For Selections:**

  ```sh
  pytest tests/test_selections.py --cov=app --cov-report=html --cov-report=term
  ```