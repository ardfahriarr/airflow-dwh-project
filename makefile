.PHONY: venv env init up down restart ps logs clean

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
ENV_FILE := .env

AIRFLOW_UID := $(shell id -u)

venv:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Creating Python virtual environment..."; \
		python3 -m venv $(VENV); \
	fi
	@$(PIP) install --quiet --upgrade pip
	@$(PIP) install --quiet cryptography

env: venv
	@echo "Creating Airflow directories..."
	@mkdir -p ./dags ./logs ./plugins ./config
	@echo "Setting permissions..."
	@chmod -R 777 ./dags ./logs ./plugins ./config

	@if [ -f "$(ENV_FILE)" ]; then \
		echo ".env already exists, skipping"; \
	else \
		echo "Creating .env..."; \
		FERNET_KEY=$$($(PYTHON) -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"); \
		ADMIN_PASSWORD=$$(openssl rand -base64 24); \
		printf '%s\n' \
			"AIRFLOW_UID=50000" \
			'' \
			'# Airflow Web User' \
			'_AIRFLOW_WWW_USER_CREATE=true' \
			'_AIRFLOW_WWW_USER_USERNAME=admin' \
			"_AIRFLOW_WWW_USER_PASSWORD=$${ADMIN_PASSWORD}" \
			'' \
			'# Airflow Fernet Key' \
			"AIRFLOW__CORE__FERNET_KEY=$${FERNET_KEY}" \
			> $(ENV_FILE); \
		echo ".env created"; \
	fi

init:
	docker compose up airflow-init

up:
	docker compose up -d

down:
	docker compose down

clean:
	docker compose down --volumes --remove-orphans