# Use the official Python 3.9 slim image
FROM python:3.9-slim

# Install system dependencies for ffmpeg, git, and libsndfile1
RUN apt-get update && apt-get install -y ffmpeg libsndfile1 git

# Install Whisper from GitHub and torch
RUN pip install git+https://github.com/openai/whisper.git && pip install torch

# Create directories for the podcast audio and transcriptions
RUN mkdir -p /app/podcast_audio /app/transcriptions

# Copy the specific transcribe_podcasts.py file from the blog_scrape folder into the /app directory
COPY blog_scrape/transcribe_podcasts.py /app/

# Set the working directory inside the container
WORKDIR /app

# Run the Python script when the container launches
CMD ["python", "transcribe_podcasts.py"]
