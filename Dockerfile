# Build a virtualenv using the appropriate Debian release
# * Install python3-venv for the built-in Python3 venv module (not installed by default)
# * Install gcc libpython3-dev to compile C Python modules
# * In the virtualenv: Update pip setuputils and wheel to support building new packages
#                      Install poetry to facilitate installation of app dependencies
FROM python:3.10.8-bullseye AS build
ARG POETRY_VERSION=1.2.2
# hadolint ignore=SC1072
RUN apt-get update && \
  apt-get install --no-install-suggests --no-install-recommends --yes python3-venv gcc libpython3-dev && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* && \
  python3 -m venv /venv && \
  /venv/bin/pip install --upgrade pip setuptools wheel && \
  /venv/bin/pip install "poetry==${POETRY_VERSION}"

# Build the requirements.txt file as a separate step: Only re-execute this step when pyproject.toml or poetry.lock change
FROM build AS build-venv
COPY pyproject.toml poetry.lock /
RUN /venv/bin/poetry export --without-hashes --with-credentials --format requirements.txt --output /requirements.txt
RUN /venv/bin/pip install --disable-pip-version-check -r /requirements.txt
    # distroless has /usr/bin/python, and python:3-alpine has /usr/local/bin/python
RUN ln -sf /usr/bin/python /venv/bin/python

FROM gcr.io/distroless/python3-debian11 AS runtime
COPY --from=build-venv /venv /venv
WORKDIR /app
COPY . /app
ENTRYPOINT ["/venv/bin/python", "/app/manage.py", "runserver"]
