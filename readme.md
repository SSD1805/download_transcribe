# **YouTube Audio Downloader and Transcriber**

This project is a modular, microservices-based application designed to:
- Download and process audio from YouTube videos.
- Transcribe audio using Whisper AI and advanced NLP techniques.
- Execute complex workflows with efficient task distribution using Celery, Dask, and optional Ray for high-performance GPU tasks.

It is scalable, containerized for easy deployment, and integrates distributed workers for efficient task management.

---

## **Features**

| Feature                      | Description                                                                                                                   |
|------------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| **Audio Download**           | Uses `yt-dlp` to download audio in `.mp3` format from videos or channels.                                                     |
| **Transcription**            | Transcribes audio with WhisperX, supporting speaker tagging and timestamps, saved as `.txt` files.                            |
| **Skip Existing Files**      | Prevents redundant downloads or processing by checking for existing audio and transcription files.                            |
| **Audio Processing**         | Converts, normalizes, splits, and trims audio using modular pipelines.                                                        |
| **Text Processing**          | Advanced NLP tasks, including Named Entity Recognition (NER), tokenization, and segmentation using spaCy and NLTK.            |
| **Configurable Pipelines**   | Centralized configuration with `config.yaml` and dynamic updates via `SettingsRegistry`.                                       |
| **Task Distribution**        | Distributed task execution with Celery, Dask, and optional Ray for scalability.                                               |
| **Containerized Architecture** | Docker-based architecture with isolated services for fault tolerance and scalability.                                         |
| **Logging and Monitoring**   | Advanced logging and performance tracking using custom trackers and configurable logging via `.env`.                          |
| **Reusable Utilities**       | Modular utilities for file operations, logging, and performance tracking to simplify integration.                             |
| **Folder Management**        | Organizes files in structured directories (`/data/audio_files`, `/data/transcriptions`) for easy access and management.        |
| **Environment Variables**    | Stores sensitive data in environment variables loaded from `.env`.                                                            |

---

## **Project Structure**

```plaintext
.
├── config                     # Configuration files
│   └── config.yaml            # Central configuration file
├── data                       # Data files and directories
│   ├── __init__.py
│   ├── audio_files            # Downloaded audio files
│   ├── processed              # Processed audio and text files
│   └── transcriptions         # Generated transcriptions
├── db                         # Database-related files (PostgreSQL)
├── docker                     # Docker configurations
│   ├── audio                  # Audio processing Dockerfiles
│   │   ├── Dockerfile_converter
│   │   ├── Dockerfile_normalizer
│   │   ├── Dockerfile_splitter
│   │   └── Dockerfile_trimmer
│   ├── celery                 # Celery Dockerfiles
│   │   ├── Dockerfile_beat
│   │   └── Dockerfile_worker
│   ├── dask_worker            # Dask worker Dockerfiles
│   │   ├── Dockerfile_audio_conversion_worker
│   │   ├── Dockerfile_dask_scheduler
│   │   ├── Dockerfile_ner_worker
│   │   ├── Dockerfile_performance_monitor_worker
│   │   ├── Dockerfile_pipeline_manager
│   │   ├── Dockerfile_text_loading_worker
│   │   ├── Dockerfile_text_saving_worker
│   │   ├── Dockerfile_text_segmentation_worker
│   │   └── Dockerfile_text_tokenization_worker
│   ├── django_app             # Django application Dockerfile
│   │   └── Dockerfile_django
│   ├── downloaders            # Download managers Dockerfiles
│   │   ├── Dockerfile_download_manager
│   │   └── Dockerfile_youtube_downloader
│   ├── reverse_proxy          # Reverse proxy for routing (Nginx)
│   │   └── Dockerfile_nginx
│   ├── text_processing        # Text processing Dockerfiles
│   │   ├── Dockerfile_loader
│   │   ├── Dockerfile_ner_processor
│   │   ├── Dockerfile_saver
│   │   ├── Dockerfile_segmenter
│   │   └── Dockerfile_tokenizer
│   └── transcription_service  # Transcription services Dockerfiles
│       ├── Dockerfile_audio_transcriber
│       ├── Dockerfile_main_transcriber
│       └── Dockerfile_transcription_saver
├── src                        # Source code
│   ├── celery_tasks           # Celery tasks for various workflows
│   │   ├── cleanup_tasks.py
│   │   ├── download_tasks.py
│   │   ├── transcription_tasks.py
│   │   └── shared_tasks.py
│   ├── cli                    # Command-line interface
│   │   └── app.py
│   ├── core                   # Core utilities and services
│   │   ├── batch_processor.py
│   │   ├── exception_handler.py
│   │   ├── memory_monitor.py
│   │   └── services.py
│   ├── dask_tasks             # Dask workers for parallel processing
│   │   ├── audio_conversion_worker.py
│   │   ├── transcription_worker.py
│   │   └── text_tokenization_worker.py
│   ├── modules                # Modular utilities
│   │   ├── audio_handler.py
│   │   ├── config_manager.py
│   │   └── transcription_manager.py
│   ├── pipelines              # Processing pipelines
│   │   ├── audio              # Audio processing pipelines
│   │   │   ├── audio_converter.py
│   │   │   ├── audio_normalizer.py
│   │   │   ├── audio_splitter.py
│   │   │   └── cli_audio.py
│   │   ├── download           # Download management
│   │   │   ├── download_handler.py
│   │   │   └── youtube_downloader.py
│   │   ├── registry           # Registry patterns for settings and models
│   │   │   ├── configuration_registry.py
│   │   │   └── model_registry.py
│   │   ├── text               # Text processing pipelines
│   │   │   ├── ner_processor.py
│   │   │   ├── text_loader.py
│   │   │   ├── text_saver.py
│   │   │   └── text_segmenter.py
│   │   └── transcription      # Transcription pipelines
│   │       ├── audio_transcriber.py
│   │       └── transcription_pipeline.py
│   └── utils                  # Shared utility scripts
│       ├── concurrency_manager.py
│       ├── file_utilities.py
│       ├── logger_service.py
│       └── yaml_parser.py
├── docker-compose.yml         # Docker Compose orchestration
├── pyproject.toml             # Poetry dependency file
└── README.md                  # Documentation

```

## **Task Mapping and Framework Selection**

### **1. Celery-Specific Tasks**
| **Task**              | **Files**                                                                                   |
|-----------------------|---------------------------------------------------------------------------------------------|
| **Video Downloading** | `src/celery_tasks/download_tasks.py`, `src/modules/download_coordinator.py`, `src/pipelines/download/youtube_downloader.py` |
| **Task Orchestration**| `src/celery_tasks/schedule.py`, `src/celery_tasks/shared_tasks.py`                          |
| **Cleanup Tasks**     | `src/celery_tasks/cleanup_tasks.py`                                                        |
| **User Requests**     | `src/django/views.py`, `src/cli/app.py`                                                    |

### **2. Dask-Specific Tasks**
| **Task**                  | **Files**                                                                                     |
|---------------------------|-----------------------------------------------------------------------------------------------|
| **Audio Processing**       | `src/dask_tasks/audio_conversion_worker.py`, `src/pipelines/audio/audio_converter.py`, `src/pipelines/audio/audio_normalizer.py` |
| **Text Processing**        | `src/dask_tasks/text_tokenization_worker.py`, `src/pipelines/text/text_tokenizer.py`, `src/pipelines/text/text_segmenter.py`     |
| **Transcription Processing**| `src/dask_tasks/transcription_worker.py`, `src/pipelines/transcription/audio_transcriber.py`                                      |
| **Performance Monitoring** | `src/dask_tasks/performance_monitor_worker.py`, `src/utils/performance_tracker.py`                                               |

### **3. Ray-Specific Tasks (Optional)**
| **Task**                   | **Files**                                                                                   |
|----------------------------|---------------------------------------------------------------------------------------------|
| **Unified Orchestration**   | Refactor existing Celery and Dask tasks using Ray APIs                                     |
| **GPU-Accelerated Tasks**   | Whisper transcription tasks with GPU support                                               |

---

## **Updated Docker Containers**

| Container                   | Purpose                                           | Benefits                                                         |
|-----------------------------|---------------------------------------------------|-----------------------------------------------------------------|
| **YouTube Downloader**      | Downloads audio using `yt-dlp`.                   | Decoupled download logic for scalability and fault isolation.   |
| **Audio Processor**         | Handles normalization, conversion, and trimming. | Modular processing pipelines for audio workflows.              |
| **Transcription Service**   | Transcribes audio with WhisperX.                  | Efficient transcription with GPU acceleration (Lambda Labs).   |
| **Text Processing Service** | Handles NLP tasks (NER, segmentation).            | Independent scaling of NLP workflows.                          |
| **Celery Worker**           | Asynchronous task processing.                     | Enables background task management.                            |
| **Dask Worker**             | Distributed processing of data tasks.             | Parallelism for computationally heavy tasks.                   |
| **Reverse Proxy (Nginx)**   | Manages SSL and request routing.                  | Provides load balancing and security.                          |
| **Database (PostgreSQL)**   | Stores metadata and transcript data.              | Reliable and scalable data storage.                            |

---

## **Technologies and Dependencies**

| Component                  | Technology            | Purpose                                     | Docker Container      |
| -------------------------- | --------------------- | ------------------------------------------- | --------------------- |
| **Framework**              | Django                | Backend structure and logic                 | Django App            |
| **Frontend**               | React or Vue          | Interactive user interface                  | Django App            |
| **API Layer**              | Django REST Framework | REST API for frontend/backend communication | Django App            |
| **Real-Time Updates**      | Django Channels       | WebSocket for real-time updates             | Django App            |
| **Task Queue**             | Celery                | Background task management                  | Celery Worker         |
| **Distributed Processing** | Dask                  | Parallel processing of heavy tasks          | Dask Worker           |
| **GPU Processing**         | Lambda Labs GPU       | Runs WhisperX model on GPU                  | Transcription Service |
| **Transcription/NLP**      | WhisperX              | ASR tool for audio transcription            | Transcription Service |
| **Data Storage**           | PostgreSQL            | Stores metadata and transcription data      | Database              |
| **Static/Media Storage**   | Linode/AWS S3         | Stores audio and transcript files           | External              |
| **NLP Libraries**          | spaCy, NLTK           | Text processing tools                       | Text Processing       |
| **Reverse Proxy**          | Nginx                 | Routes requests and handles SSL             | Reverse Proxy         |
| **Logging**                | Django Logging        | Logs events and errors                      | Django App            |
| **Monitoring**             | Grafana, Prometheus   | Application performance monitoring          | Optional              |

---

## **Usage**

### Run with Docker Compose
```bash
docker-compose up --build
```

---

### CLI Commands
| Command          | Description                       | Example Usage                                        |
|------------------|-----------------------------------|-----------------------------------------------------|
| **download**     | Downloads YouTube audio.          | `poetry run python app.py download --url <URL>`      |
| **transcribe**   | Transcribes an audio file.        | `poetry run python app.py transcribe <file>`         |
| **process**      | NLP processing on transcriptions. | `poetry run python app.py process --directory <dir>` |

---

## **Future Goals**

1. **Enhance Scalability**:
   - Transition to Ray for unified scaling across I/O and CPU/GPU tasks.
2. **Simplify Architecture**:
   - Evaluate whether a hybrid approach (Celery + Dask) remains necessary or if Ray can simplify workflows.
3. **Optimize Performance**:
   - Profile tasks to ensure efficient use of resources across all frameworks.

--- 

