# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /app

# Install Poetry
RUN pip install --upgrade pip && \
    pip install poetry

# Copy dependency files first
COPY pyproject.toml poetry.lock /app/

# Install dependencies using Poetry
RUN poetry config virtualenvs.create true && poetry install --no-dev

# Copy the application code
COPY . .

# Stage 2: Runner
FROM python:3.11-slim

WORKDIR /app

# Copy the environment from the builder stage
COPY --from=builder /app /app

# Expose any required ports here
EXPOSE 8000

# Run the application (adjust the command to your specific needs)
CMD ["poetry", "run", "python", "src/cli/cli_audio.py"]
