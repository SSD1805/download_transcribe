# Use the official Python 3.12 slim Bookworm image as the base image
FROM python:3.12-slim-bookworm AS base

# Install system dependencies with limited packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    libsndfile1 \
    gcc \
    libssl-dev \
    libffi-dev \
    libasound2-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the pyproject.toml and poetry.lock for dependency installation
COPY pyproject.toml poetry.lock /app/

# Install Poetry
RUN pip install --upgrade pip && \
    pip install poetry

# Install Python dependencies using Poetry
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# Install spaCy and its model
RUN poetry run pip install spacy && \
    poetry run python -m spacy download en_core_web_sm

# Install development dependencies
RUN poetry install --with dev

# Copy the rest of the application code
COPY src /app

# Set up directories for audio files and transcriptions
RUN mkdir -p /app/audio_files /app/transcriptions /app/logs

# Default environment variables
ENV FFMPEG_PATH="/usr/bin/ffmpeg" \
    WHISPER_MODEL_SIZE="base" \
    TRANSCRIPTION_FORMAT="txt" \
    LOG_FILE_PATH="/app/logs/my_app.log" \
    LOG_LEVEL="10" \
    LOG_MAX_BYTES="10485760" \
    LOG_BACKUP_COUNT="5" \
    ENABLE_CONSOLE_LOGGING="true" \
    ENABLE_FILE_LOGGING="true"

# Command to run the main app.py file as the entry point
CMD ["poetry", "run", "python", "/app/app.py"]