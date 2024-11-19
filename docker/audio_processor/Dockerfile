# Base image
FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y ffmpeg \
    && pip install --no-cache-dir poetry

# Copy application code
WORKDIR /app
COPY . .

# Install dependencies via Poetry
RUN poetry install --no-dev

# Entry point for multi-task processing
ENTRYPOINT ["poetry", "run", "python", "src/cli/app.py"]
