# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /app

# Install Poetry and dependencies
RUN pip install --upgrade pip && pip install poetry
COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create true && poetry install --no-dev

# Copy the application code
COPY . .

# Stage 2: Runner
FROM python:3.11-slim

WORKDIR /app

# Copy the environment from the builder stage
COPY --from=builder /app /app

# Load environment variables from .env file
COPY .env /app/.env

# Run the transcription service script
CMD ["poetry", "run", "python", "src/cli/cli_transcription_service.py"]
