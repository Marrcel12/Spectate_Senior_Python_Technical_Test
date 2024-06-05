DOCKER_COMPOSE = docker-compose
DOCKER_COMPOSE_FILE = 2_REST_Application/docker-compose.yml
FLASK_APP = 2_REST_Application
FLASK_ENV = development
ENV:=env

.PHONY: help build up down migrate run_local lint

help: ## Show this help message
	@echo "Makefile commands:"
	@echo "make build       - Build Docker containers"
	@echo "make up          - Start the app from zero with Docker"
	@echo "make down        - Stop the Docker containers"
	@echo "make migrate     - Apply migrations using Alembic"
	@echo "make run_local   - Run the app locally"
	@echo "make lint        - Lint the code with Black"

build: 
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) build
up: build 
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up -d
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) run migrate
down: 
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down

migrate: 
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) run migrate

# This part working only for windows and is for developing purpose
env:
	python -m venv $(ENV) 
	.\$(ENV)\Scripts\pip install --no-cache-dir -r $(FLASK_APP)/requirements.txt 

install_local:
	pip install --no-cache-dir -r $(FLASK_APP)/requirements.txt

migrate_local:
	cd $(FLASK_APP)
	.\$(ENV)\Scripts\alembic upgrade head

lint: 	
	.\$(ENV)\Scripts\isort $(FLASK_APP) 
	.\$(ENV)\Scripts\black $(FLASK_APP)

run_local: 
	cd $(FLASK_APP)	
	.\$(ENV)\Scripts\flask run