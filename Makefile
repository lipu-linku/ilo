MAIN=podman
SUB=podman-compose
# MAIN=docker
# SUB=docker compose

init:
	pdm install
	# pdm run pre-commit install

test:
	pdm run pytest -rP ./tests

build:
	${SUB} build

up:
	${SUB} up -d

local:
	pdm run python -m ilo

stop:
	${SUB} stop

down:
	${SUB} down

logs:
	${SUB} logs

import:
	# container must be running
	${MAIN} cp ./userdata/preferences.json $(shell ${MAIN} ps | grep ilo-linku | awk '{print $$1}'):/project/userdata/preferences.json

export:
	# container must be running
	${MAIN} cp $(shell ${MAIN} ps | grep ilo-linku | awk '{print $$1}'):/project/userdata/preferences.json ./userdata/preferences.json
