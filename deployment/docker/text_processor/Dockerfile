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
COPY --from=builder /app /app

# Run the text_processing processing service
CMD ["poetry", "run", "python", "src/cli/cli_text_processor.py"]
