FROM python:3.9

# Set to "dev" for dev deps
ARG STAGE="production"

ENV STAGE=${STAGE} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.5.1 \
  POETRY_HOME="/usr/local/poetry"

RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y curl gcc make && \
  rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python - --version 1.5.1 \
  && ln -sf /usr/local/poetry/bin/poetry /usr/local/bin/poetry

# Install dependencies.
COPY poetry.lock pyproject.toml /app/

WORKDIR /app
RUN poetry config virtualenvs.create false && \
  poetry install --no-interaction --no-ansi --no-root $(/usr/bin/test $STAGE == production && echo "--without dev")

# Install the project.
COPY . /app/
RUN poetry install  --no-interaction --no-ansi $(/usr/bin/test $STAGE == production && echo "--without dev")

EXPOSE 8000
ENV PORT=8000
CMD ["sh","-c","poetry run fastapi run /app/kharon/app.py --host 0.0.0.0 --port 8000"]
