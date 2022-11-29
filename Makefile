init:
	pdm install
	pdm run pre-commit install

test:
	pdm run pytest -rP ./tests

build:
	docker compose build

up:
	docker compose up -d

local:
	pdm run python -m ilo

down:
	docker compose down

logs:
	docker compose logs

import:
	# container must be running
	docker cp ./userdata/preferences.json $(shell docker ps | grep ilo-bot | awk '{print $$1}'):/project/userdata/preferences.json

export:
	# container must be running
	docker cp $(shell docker ps | grep ilo-bot | awk '{print $$1}'):/project/userdata/preferences.json ./userdata/preferences.json
