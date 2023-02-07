MAIN=podman
SUB=podman-compose
# MAIN=docker
# SUB=docker compose

init:
	pdm install
	# pdm run pre-commit install

test:
	pdm run pytest -vvrP ./tests

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
