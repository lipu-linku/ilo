FROM python:3.13-slim-trixie AS builder

COPY src /project/src
COPY pyproject.toml uv.lock /project

WORKDIR /project
ENV UV_PYTHON_DOWNLOADS=0
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_NO_DEV=1
RUN --mount=from=ghcr.io/astral-sh/uv:0.12,source=/uv,target=/bin/uv \
    --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable

FROM python:3.13-slim-trixie
RUN apt-get update -y && \
  apt-get install -y --no-install-recommends \
  libfribidi0 \
  libraqm0 && \
  apt-get autoclean -y && \
  apt-get autoremove -y

COPY ijo/nasinsitelen/ /project/ijo/nasinsitelen/
COPY kemeka/data/ /project/kemeka/data/

COPY --from=builder /project/.venv /project/.venv

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /project

CMD [".venv/bin/python", "-m", "ilo"]
