### celery_app.py ###
from celery import Celery

# Create Celery app instance using ConfigurationRegistry
celery_app = Celery(
    "youtube_audio_downloader",
    broker=container.configuration_registry()
    .get("celery", {})
    .get("broker_url", "redis://localhost:6379/0"),
    backend=container.configuration_registry()
    .get("celery", {})
    .get("result_backend", "django-db"),
)

# Load configuration from ConfigurationRegistry
celery_config = container.configuration_registry().get("celery", {})

celery_app.conf.update(
    task_serializer=celery_config.get("task_serializer", "json"),
    accept_content=celery_config.get("accept_content", ["json"]),
    result_serializer=celery_config.get("result_serializer", "json"),
    timezone=celery_config.get("timezone", "UTC"),
    enable_utc=celery_config.get("enable_utc", True),
    task_track_started=celery_config.get("task_track_started", True),
    task_time_limit=celery_config.get("task_time_limit", 300),
)

# Discover tasks from specific modules
celery_app.autodiscover_tasks(
    [
        "src.celery.cleanup_tasks",
        "src.celery.download_tasks",
        "src.celery.transcription_tasks",
        "src.celery.shared_tasks",
    ]
)
