MAIN=podman
SUB=podman-compose
# MAIN=docker
# SUB=docker compose

init:
	uv sync

test:
	uv run pytest

build:
	${SUB} build

up:
	${SUB} up -d

local:
	uv run -m ilo

stop:
	${SUB} stop

down:
	${SUB} down

logs:
	${SUB} logs
