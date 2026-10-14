# syntax=docker/dockerfile:1

# ---------- Stage 1: build the virtual environment ----------
    FROM python:3.12-slim AS builder

    COPY --from=ghcr.io/astral-sh/uv:0.12.23 /uv /uvx /bin/

    ENV UV_COMPILE_BYTECODE=1 \
        UV_LINK_MODE=copy \
        UV_PYTHON_DOWNLOADS=0

    WORKDIR /app

    # 1) Dependencies only. This layer is cached until uv.lock or pyproject.toml changes.
    RUN --mount=type=cache,target=/root/.cache/uv \
        --mount=type=bind,source=uv.lock,target=uv.lock \
        --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
        uv sync --locked --no-install-project --no-dev

    # 2) The project itself. Rebuilt whenever source code changes.
    COPY . /app
    RUN --mount=type=cache,target=/root/.cache/uv \
        uv sync --locked --no-dev --no-editable


    # ---------- Stage 2: the small runtime image ----------
    FROM python:3.12-slim AS runtime

    LABEL org.opencontainers.image.title="plantassist" \
          org.opencontainers.image.description="Local-LLM RAG troubleshooting assistant for industrial equipment" \
          org.opencontainers.image.source="https://github.com/wez1102/industrial-ai-troubleshooting" \
          org.opencontainers.image.licenses="MIT"

    RUN groupadd --system --gid 1001 app \
     && useradd --system --uid 1001 --gid app --no-create-home app

    WORKDIR /app

    COPY --from=builder /app/.venv /app/.venv
    COPY alembic.ini /app/alembic.ini
    COPY migrations /app/migrations

    ENV PATH="/app/.venv/bin:$PATH" \
        PYTHONUNBUFFERED=1 \
        PYTHONDONTWRITEBYTECODE=1

    USER app

    EXPOSE 8000

    HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
        CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health/live', timeout=2)"]

    CMD ["uvicorn", "plantassist.main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
