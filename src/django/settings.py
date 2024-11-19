import os
import environ
import structlog
from celery.signals import setup_logging

# Base Directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Initialize environment variables
env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
)

# Read .env file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Security settings
DEBUG = env("DEBUG")
SECRET_KEY = env("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# Database configuration
DATABASES = {
    "default": env.db(),  # Reads DATABASE_URL from .env
}

# Whisper Configuration
WHISPER_MODEL_SIZE = env("WHISPER_MODEL_SIZE", default="base")
DEVICE = env("DEVICE", default="cpu")

# WhisperX Configuration
WHISPERX_ALIGNMENT_ENABLED = env.bool("ALIGNMENT_ENABLED", default=True)
WHISPERX_DIARIZATION_ENABLED = env.bool("DIARIZATION_ENABLED", default=True)

# Celery Configuration
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "django-db"  # Or another backend like Redis
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"
CELERY_ENABLE_UTC = True
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 300  # Task timeout in seconds

# Structlog Configuration
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

@setup_logging.connect
def configure_structlog_celery(**kwargs):
    """Configure Structlog for Celery."""
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

# Logging Configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "app.log"),
            "formatter": "verbose",
        },
        "structlog_console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True,
        },
        "celery": {  # Celery-specific logging
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True,
        },
        "custom_logger": {  # For custom logging
            "handlers": ["console", "file", "structlog_console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
