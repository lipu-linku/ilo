FROM python:3.11-slim AS builder
RUN python -m pip install --no-cache-dir pdm
RUN pdm config python.use_venv false

COPY pyproject.toml pdm.lock /project/
WORKDIR /project
RUN pdm install --prod --no-lock --no-editable

FROM python:3.11-slim AS bot
# NOTE: this is NOT optimized.
# Ideally the build could be done in another image and copied here
RUN apt-get update -y && \
  apt-get install -y --no-install-recommends \
  libfribidi0 \
  meson pkg-config ragel gtk-doc-tools gcc g++ libfreetype6-dev libglib2.0-dev libcairo2-dev \
  apt-transport-https ca-certificates \
  ninja-build \
  git \
  && \
  apt-get autoclean -y && \
  apt-get autoremove -y

RUN git clone --single-branch --depth 1 -b random-state https://github.com/harfbuzz/harfbuzz.git /tmp/harfbuzz
WORKDIR /tmp/harfbuzz
RUN meson build
RUN meson compile -C build
WORKDIR /tmp/harfbuzz/build
RUN meson install

ENV PYTHONPATH=/project/pkgs

COPY src/ /project/pkgs/
COPY ijo/nasinsitelen/ /project/ijo/nasinsitelen

# this will change most often
COPY --from=builder /project/__pypackages__/3.11/lib /project/pkgs
WORKDIR /project
ENTRYPOINT ["python", "-m", "ilo"]
