
# YouTube Audio Downloader and Transcriber

This project is a microservices-based application designed to download audio from YouTube videos, transcribe it using Whisper AI, and process the transcriptions for further analysis. It is modular, scalable, and fully containerized for easy deployment.

## Features

| Feature                     | Description                                                                                                                                   |
|-----------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| **Audio Download**          | Uses `yt-dlp` to download audio in `.mp3` format from videos or channels.                                                                    |
| **Transcription**           | Transcribes audio with WhisperX, supporting speaker tagging and timestamps, saved as `.txt` files.                                          |
| **Skip Existing Files**     | Prevents redundant downloads or processing by checking for existing audio and transcription files.                                           |
| **Modular Structure**       | Organized into modules for audio processing, transcription, configuration, and text processing, ensuring a scalable codebase.                |
| **Text Processing**         | Includes Named Entity Recognition (NER) with spaCy and sentence segmentation with NLTK.                                                     |
| **Folder Management**       | Manages files in structured directories (`/app/audio_files`, `/app/transcriptions`).                                                        |
| **Configurable**            | Central configuration with `config.yaml` for customizable settings (e.g., download delay, model size).                                      |
| **Logging**                 | Configurable logging based on `.env`, supporting both console and file logging.                                                             |
| **Environment Variables**   | Sensitive data is stored in environment variables loaded from `.env`.                                                                       |
| **Containerized**           | Docker-based architecture allows each component to run in separate containers for modularity and fault isolation.                          |

## Project Structure

```plaintext
download_transcribe/
├── .venv/                       # Python virtual environment
├── app/
│   ├── audio_files/             # Downloaded audio files
│   └── transcriptions/          # Generated transcriptions
├── db/                          # Database-related files
├── docker/
│   ├── audio_processing/
│   │   ├── Dockerfile_audio_converter
│   │   ├── Dockerfile_audio_normalizer
│   │   ├── Dockerfile_audio_splitter
│   │   └── Dockerfile_audio_trimmer
│   ├── celery_worker/
│   │   └── Dockerfile_celery
│   ├── dask_worker/
│   │   └── Dockerfile_dask
│   ├── django_app/
│   │   └── Dockerfile_django
│   ├── downloaders/
│   │   ├── Dockerfile_download_manager
│   │   └── Dockerfile_youtube_downloader
│   ├── reverse_proxy/
│   │   └── Dockerfile_nginx
│   ├── text_processing/
│   │   ├── Dockerfile_ner_processor
│   │   ├── Dockerfile_text_loader
│   │   ├── Dockerfile_text_saver
│   │   ├── Dockerfile_text_segmenter
│   │   └── Dockerfile_text_tokenizer
│   └── transcription_service/
│       ├── Dockerfile_audio_transcriber
│       ├── Dockerfile_main_transcriber
│       └── Dockerfile_transcription_saver
├── src/
│   ├── audio_pipeline/
│   │   ├── audio_converter.py
│   │   ├── audio_normalizer.py
│   │   ├── audio_splitter.py
│   │   ├── audio_trimmer.py
│   │   └── cli_audio.py
│   ├── cli/
│   │   └── app.py
│   ├── core/
│   │   ├── batch_processor.py
│   │   ├── file_manager.py
│   │   ├── file_uploader.py
│   │   ├── logger_manager.py
│   │   ├── memory_monitor.py
│   │   └── performance_tracker.py
│   ├── download_pipeline/
│   │   ├── download_manager.py
│   │   └── youtube_downloader.py
│   ├── modules/
│   │   ├── audio_handler.py
│   │   ├── config_manager.py
│   │   ├── download_coordinator.py
│   │   ├── helper_functions.py
│   │   ├── pipeline_manager.py
│   │   ├── text_processor.py
│   │   └── transcription_manager.py
│   ├── text_pipeline/
│   │   ├── ner_processor.py
│   │   ├── text_loader.py
│   │   ├── text_saver.py
│   │   ├── text_segmenter.py
│   │   └── text_tokenizer.py
│   ├── transcription_pipeline/
│   │   ├── audio_transcriber.py
│   │   ├── main_transcriber.py
│   │   └── transcription_saver.py
│   └── utils/
│       ├── filename_sanitizer.py
│       ├── message_logger.py
│       ├── progress_bar.py
│       └── timestamp_formatter.py
├── tests/                       # Test cases
├── .env                         # Environment variables
├── config.yaml                  # Application configuration
├── docker-compose.yml           # Docker Compose for services
├── Dockerfile                   # Base Dockerfile
├── pyproject.toml               # Poetry dependency file
└── README.md                    # Documentation
```

## Docker Containers

| Container                   | Purpose                                              | Benefits                                                                                        |
|-----------------------------|------------------------------------------------------|--------------------------------------------------------------------------------------------------|
| **YouTube Downloader**      | Downloads YouTube audio using `yt-dlp`.              | Handles video/audio download requests independently.                                            |
| **Audio Converter**         | Converts downloaded audio to the required format.    | Isolated audio conversion, enabling scalable audio tasks.                                       |
| **Audio Normalizer**        | Normalizes audio levels.                             | Ensures consistent audio quality across files.                                                  |
| **Audio Splitter**          | Splits audio into smaller segments if necessary.     | Enables modular processing of audio.                                                            |
| **Audio Trimmer**           | Trims silence or unwanted sections in audio.         | Ensures cleaner and more concise audio files.                                                   |
| **Transcription Service**   | Transcribes audio with WhisperX.                     | GPU-enabled for efficient transcription tasks.                                                  |
| **Text Processing Modules** | NLP tasks (NER, segmentation).                       | Independent scaling and updates for NLP processes.                                              |
| **Django App**              | Main web application and API backend.                | Centralized interface for UI, authentication, and API handling.                                 |
| **Celery Worker**           | Asynchronous task processing.                        | Offloads background tasks from Django app to keep it responsive.                                |
| **Dask Worker**             | Distributed processing of data tasks.                | Parallel processing for computationally heavy tasks.                                            |
| **Reverse Proxy (Nginx)**   | Manages SSL and request routing.                     | Provides load balancing and security.                                                           |
| **Database (PostgreSQL)**   | Stores metadata and transcript data.                 | Reliable storage for metadata and transcription files.                                          |

## Technologies and Dependencies

| Component                  | Technology               | Purpose                                       | Docker Container     |
|----------------------------|--------------------------|-----------------------------------------------|-----------------------|
| **Framework**              | Django                   | Backend structure and logic                  | Django App           |
| **Frontend**               | React or Vue             | Interactive user interface                    | Django App           |
| **API Layer**              | Django REST Framework    | REST API for frontend/backend communication   | Django App           |
| **Real-Time Updates**      | Django Channels          | WebSocket for real-time updates               | Django App           |
| **Task Queue**             | Celery                   | Background task management                    | Celery Worker        |
| **Distributed Processing** | Dask                     | Parallel processing of heavy tasks            | Dask Worker          |
| **GPU Processing**         | Paperspace/AWS GPU       | Runs WhisperX model on GPU                    | Transcription Service |
| **Transcription/NLP**      | WhisperX                 | ASR tool for audio transcription              | Transcription Service |
| **Data Storage**           | PostgreSQL               | Stores metadata and transcription data        | Database             |
| **Static/Media Storage**   | Linode/AWS S3            | Stores audio and transcript files             | External             |
| **NLP Libraries**          | spaCy, NLTK              | Text processing tools                         | Text Processing      |
| **Reverse Proxy**          | Nginx                    | Routes requests and handles SSL               | Reverse Proxy        |
| **Logging**                | Django Logging           | Logs events and errors                        | Django App           |
| **Monitoring**             | Grafana, Prometheus      | Application performance monitoring            | Optional             |

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Install Dependencies Using Poetry

```bash
poetry install
```

### 3. Install `ffmpeg`

Follow the instructions for your OS to install `ffmpeg`.

## Usage

### Run with Docker Compose

To build and start all services:

```bash
docker-compose up --build
```

To stop the services:

```bash
docker-compose down
```

### CLI Commands

| Command         | Description                           |

 Example Usage                                      |
|-----------------|---------------------------------------|----------------------------------------------------|
| **download**    | Downloads YouTube audio.             | `poetry run python app.py download --url <URL>`    |
| **transcribe**  | Transcribes an audio file.           | `poetry run python app.py transcribe <file>`       |
| **process**     | NLP processing on transcriptions.    | `poetry run python app.py process --directory <dir>`|
| **setup**       | Configures the application.          | `poetry run python app.py setup`                   |
| **manage_files**| Manages files in a directory.        | `poetry run python app.py manage_files <directory>`|

### Sample Workflow

```bash
# Full Workflow
poetry run python data.py download --url "https://youtube.com/your-video"
poetry run python data.py transcribe /data/audio_files/downloaded_audio.mp3
poetry run python data.py process --directory "/app/transcriptions"
```

## Configuration

Modify `config.yaml` to set preferences like download delay, directories, and Whisper model size.

## Logging Configuration

Define logging settings in `.env`:

```plaintext
LOG_FILE_PATH=/app/logs/app.log
LOG_LEVEL=10
LOG_MAX_BYTES=10485760
LOG_BACKUP_COUNT=5
ENABLE_CONSOLE_LOGGING=true
ENABLE_FILE_LOGGING=true
```

## Testing

Run tests with:

```bash
pytest tests/
```

---

## Docker Compose Setup

### Environment Variables

Create an `.env` file to specify sensitive data:

```bash
PAPERSERVE_API_KEY=your_paperserve_api_key
DJANGO_SECRET_KEY=your_django_secret_key
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_db
```

### Starting Services

To build and launch the application:

```bash
docker-compose up --build
```

Access the app at `http://localhost:8000`.



