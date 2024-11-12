# Use the official Python 3.12 slim Bookworm image as the base image
FROM python:3.12-slim-bookworm AS base

# Install system dependencies
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

# Configure Poetry to install dependencies directly without a virtual environment
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# Install spaCy and its model
RUN poetry run pip install spacy && \
    poetry run python -m spacy download en_core_web_sm

# Copy the rest of the application code
COPY . /app

# Expose the port your application runs on
EXPOSE 8000

# Run the application
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]