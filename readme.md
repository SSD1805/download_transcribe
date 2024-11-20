# **YouTube Audio Downloader and Transcriber**

This project is a modular, microservices-based application designed to:
- Download and process audio from YouTube videos.
- Transcribe audio using Whisper AI and advanced NLP techniques.
- Execute complex workflows with efficient task distribution using Celery, Dask, and optional Ray for high-performance GPU tasks.

It is scalable, containerized for easy deployment, and integrates distributed workers for efficient task management.

---

## **Features**

| Feature                        | Description                                                                                                             |
|--------------------------------|-------------------------------------------------------------------------------------------------------------------------|
| **Custom Logging with Structlog** | Uses Structlog for structured logging, making it easier to filter, search, and analyze log data.                         |

| Feature                        | Description                                                                                                             |
|--------------------------------|-------------------------------------------------------------------------------------------------------------------------|
| **Audio Download**             | Uses `yt-dlp` to download audio in `.mp3` format from videos or channels.                                               |
| **Transcription**              | Transcribes audio with WhisperX as the primary tool, with Whisper AI available as a failover option, supporting speaker tagging and timestamps, saved as `.txt` files.                      |
| **Skip Existing Files**        | Prevents redundant downloads or processing by checking for existing audio and transcription files.                      |
| **Audio Processing**           | Converts, normalizes, splits, and trims audio using modular pipelines.                                                  |
| **Text Processing**            | Advanced NLP tasks, including Named Entity Recognition (NER), tokenization, and segmentation using spaCy and NLTK.      |
| **Configurable Pipelines**     | Centralized configuration with `config.yaml` and dynamic updates via `SettingsRegistry`.                                |
| **Task Distribution**          | Distributed task execution with Celery, Dask, and optional Ray for scalability.                                         |
| **Containerized Architecture** | Docker-based architecture with isolated services for fault tolerance and scalability.                                   |
| **Logging and Monitoring**     | Advanced logging and performance tracking using custom trackers and configurable logging via `.env`.                    |
| **Reusable Utilities**         | Modular utilities for file operations, logging, and performance tracking to simplify integration.                       |
| **Folder Management**          | Organizes files in structured directories (`/data/audio_files`, `/data/transcriptions`) for easy access and management. |
| **Environment Variables**      | Stores sensitive data in environment variables loaded from `.env`.                                                      |
| **Flexible Settings**          | Supports different settings for development, testing, and production environments for greater flexibility.              |

---

This is a work in progress, so some features may not be fully functional yet.

## **Getting Started**

To run this project locally, follow these steps:

### Prerequisites
- Docker and Docker Compose installed
- Python 3.x installed
- Poetry for dependency management

### Installation

1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install dependencies using Poetry:
   ```sh
   poetry install
   poetry shell
   ```

3. Set up Docker containers:
   ```sh
   docker-compose up -d
   ```

### Running the Application
- Once the containers are up, you can start the Django server by navigating to the `src` directory and running:
  ```sh
  python manage.py runserver
  ```

---

## Current Project Setup Progress

The following setup steps have been completed:

### General Setup
- **Project Structure**: The project includes a typical Django setup with Docker integration and dependencies managed through Poetry.
- **Dependency Management**: Dependencies are managed via Poetry (`poetry.lock` and `pyproject.toml` are present).
  - Installed dependencies using `poetry install`.
  - Activated the environment using `poetry shell`.
- **Docker Setup**: Docker configuration files are present.
  - The `docker-compose.yml` file defines services for Django and the database.
  - Docker volume mappings and environment variables need verification for proper configuration.

### Django Application Setup
- **Source Code**: The `src` folder contains the Django application code.
  - Initial inspection completed to verify presence of `models.py`, `views.py`, and `urls.py` for each app.
  - Ensured that the apps are registered in `INSTALLED_APPS` in `settings.py`.
- **Configuration**:
  - Verified the structure of the `config` folder, which contains environment-specific settings.
  - The database configuration and other settings in `settings.py` will be set up in subsequent steps.

### Additional Notes
- **Data Directory**: The `data` folder is currently empty. This is expected, and data population steps will follow in subsequent setup stages.
- **.gitignore**: The `.gitignore` file is being reviewed to ensure all unnecessary files are excluded from version control.
- **IDE Files**: `.idea/` is included in the project structure. It will be ignored in version control unless shared IDE settings are required.

### Next Steps
- **Database Setup**: Run `python manage.py makemigrations` and `python manage.py migrate` to configure the database.
- **Environment Variables**: Create and configure a `.env` file to store sensitive information (e.g., `DATABASE_URL`, `SECRET_KEY`).
- **Final Docker Configuration**: Verify Docker services and environment variables.

---

## **Project Structure**

```plaintext
.
├── config                     # Configuration files
│   └── config.yaml            # Central configuration file
├── data                       # Data files and directories
│   ├── audio_files            # Downloaded audio files
│   ├── processed              # Processed audio and text files
│   └── transcriptions         # Generated transcriptions
├── db                         # Database-related files (PostgreSQL)
├── docker                     # Docker configurations
│   ├── audio                  # Audio processing Dockerfiles
│   ├── celery                 # Celery Dockerfiles
│   ├── dask_worker            # Dask worker Dockerfiles
│   ├── django_app             # Django application Dockerfile
│   ├── downloaders            # Download managers Dockerfiles
│   ├── reverse_proxy          # Reverse proxy for routing (Nginx)
│   └── transcription_service  # Transcription services Dockerfiles
├── src                        # Source code
│   ├── celery_tasks           # Celery tasks for various workflows
│   ├── cli                    # Command-line interface
│   ├── core                   # Core utilities and services
│   ├── dask_tasks             # Dask workers for parallel processing
│   ├── modules                # Modular utilities
│   ├── pipelines              # Processing pipelines
│   └── utils                  # Shared utility scripts
├── docker-compose.yml         # Docker Compose orchestration
├── pyproject.toml             # Poetry dependency file
└── README.md                  # Documentation
```

---

## **Technology Stack**

| Component                  | Technology            | Purpose                                     |
|----------------------------|-----------------------|---------------------------------------------|
| **Framework**              | Django                | Backend structure and logic                 |
| **API Layer**              | Django REST Framework | REST API for frontend/backend communication |
| **Task Queue**             | Celery                | Background task management                  |
| **Distributed Processing** | Dask                  | Parallel processing of heavy tasks          |
| **Transcription/NLP**      | WhisperX (Primary) / Whisper AI (Failover) | ASR tool for audio transcription            |
| **Data Storage**           | PostgreSQL            | Stores metadata and transcription data      |
| **Static/Media Storage**   | AWS S3                | Stores audio and transcript files           |
| **Reverse Proxy**          | Nginx                 | Routes requests and handles SSL             |
| **Logging**                | Structlog              | Logs events and errors                      |

---

## **Docker Containers**

| Container                   | Purpose                                          | Benefits                                                      |
|-----------------------------|--------------------------------------------------|---------------------------------------------------------------|
| **YouTube Downloader**      | Downloads audio using `yt-dlp`.                  | Decoupled download logic for scalability and fault isolation. |
| **Audio Processor**         | Handles normalization, conversion, and trimming. | Modular processing pipelines for audio workflows.             |
| **Transcription Service**   | Transcribes audio with WhisperX.                 | Efficient transcription with GPU acceleration.                |
| **Text Processing Service** | Handles NLP tasks (NER, segmentation).           | Independent scaling of NLP workflows.                         |
| **Celery Worker**           | Asynchronous task processing.                    | Enables background task management.                           |
| **Dask Worker**             | Distributed processing of data tasks.            | Parallelism for computationally heavy tasks.                  |
| **Reverse Proxy (Nginx)**   | Manages SSL and request routing.                 | Provides load balancing and security.                         |
| **Database (PostgreSQL)**   | Stores metadata and transcript data.             | Reliable and scalable data storage.                           |

---

## **Task Mapping**

### **Celery-Specific Tasks**
| **Task**               | **Files**                                           |
|------------------------|-----------------------------------------------------|
| **Video Downloading**  | `src/celery_tasks/download_tasks.py`                |
| **Task Orchestration** | `src/celery_tasks/shared_tasks.py`                  |
| **Cleanup Tasks**      | `src/celery_tasks/cleanup_tasks.py`                 |

### **Dask-Specific Tasks**
| **Task**              | **Files**                                           |
|-----------------------|-----------------------------------------------------|
| **Audio Processing**  | `src/dask_tasks/audio_conversion_worker.py`         |
| **Text Processing**   | `src/dask_tasks/text_tokenization_worker.py`        |
| **Transcription**     | `src/dask_tasks/transcription_worker.py`            |

---

## **CLI Commands**

| Command        | Description                       | Example Usage                                        |
|----------------|-----------------------------------|------------------------------------------------------|
| **download**   | Downloads YouTube audio.          | `poetry run python app.py download --url <URL>`      |
| **transcribe** | Transcribes an audio file.        | `poetry run python app.py transcribe <file>`         |
| **process**    | NLP processing on transcriptions. | `poetry run python app.py process --directory <dir>` |

---

## **Why This Project is Cool**

- **Scalable Architecture**: The project leverages Docker containers and distributed task management with Celery and Dask, making it scalable to handle large workloads.
- **Flexible Configuration**: Supports different configurations for development, testing, and production environments, allowing easy adaptation to various use cases.
- **Advanced Transcription**: Utilizes Whisper AI for accurate and efficient audio transcription, along with NLP features for text processing.
- **Modular Design**: Each component, from downloading to processing, is modular, making it easy to extend, modify, or replace parts of the pipeline.
- **Integrated Task Distribution**: With Celery for task queue management and Dask for distributed processing, the project efficiently handles computationally intensive tasks.
- **Developer-Friendly**: The use of Poetry for dependency management and a clear project structure makes it easy for developers to get started and contribute.

---

## **Next Steps**

- **Database Setup**: Run `python manage.py makemigrations` and `python manage.py migrate` to configure the database.
- **Environment Variables**: Create and configure a `.env` file to store sensitive information (e.g., `DATABASE_URL`, `SECRET_KEY`).
- **Final Docker Configuration**: Verify Docker services and environment variables.
