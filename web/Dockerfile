FROM python:3.12-slim as base
WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=2.1.3 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# Install poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# --- Test Stage ---
FROM base as test
# Install all dependencies (main + dev)
RUN poetry install --no-root
COPY . .
# Default command to run tests
CMD ["pytest"]

# --- Production Stage ---
FROM base as prod
# Install only main dependencies
RUN poetry install --only main --no-root
COPY . .
CMD ["python", "start.py"]
