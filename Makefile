# Local use only
SHELL := /bin/bash # Use bash syntax

run:
	@uvicorn --factory app:create_app \
		--host=0.0.0.0 --port=8000 \
		--log-config=config/log-config.yml

install:
	@pip install -r requirements-dev.txt

test:
	@pytest

format:
	# @isort app && black app && \
	# isort tests && black tests
	@isort app && ruff format

generate_migration:
	alembic -c config/alembic.ini revision --autogenerate -m "$(DESCRIPTION)"

migrate:
	alembic -c config/alembic.ini upgrade head

downgrade:
	alembic -c config/alembic.ini downgrade base

install_precommit:
	pre-commit install