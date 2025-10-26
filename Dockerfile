# Copyright (c) 2025 Mikheil Tabidze
# ---------- Builder stage ----------
FROM python:3.14-slim-bookworm AS builder

# Set environment variables
ENV POETRY_VERSION=2.2.1 \
    POETRY_VIRTUALENVS_CREATE=true \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Set the working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry==${POETRY_VERSION}

# Copy poetry files and install dependencies in virtual environment
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --only=main && rm -rf $POETRY_CACHE_DIR


# ---------- Runtime stage ----------
FROM python:3.14-slim-bookworm AS runtime

# Add metadata labels
LABEL org.opencontainers.image.title="tooltility" \
      org.opencontainers.image.description="A lightweight internal web app of small, safe utilities built with Streamlit." \
      org.opencontainers.image.version="0.0.1" \
      org.opencontainers.image.authors="Mikheil Tabidze <m.tabidze@gmail.com>" \
      org.opencontainers.image.url="https://github.com/mtabidze/tooltility" \
      org.opencontainers.image.source="https://github.com/mtabidze/tooltility" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.vendor="Mikheil Tabidze"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Copy the virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Set up a non-root user for the container
RUN addgroup --system user \
    && adduser --system --group user

# Copy the app code and set proper ownership
COPY --chown=user:user app/src ./

# Expose the port
EXPOSE 8501

# Specify container health check (retries/timeout managed by Docker)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD ["python", "healthcheck.py", "http://localhost:8501/_stcore/health"]

# Switch to the non-root user for running the application
USER user

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", \
            "--client.showErrorDetails=none", \
            "--client.toolbarMode=minimal", \
            "--server.headless=true", \
            "--browser.gatherUsageStats=false"]
