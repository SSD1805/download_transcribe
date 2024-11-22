import pendulum
from celery.schedules import crontab
from dependency_injector.wiring import Provide, inject

from src.infrastructure.app.app_container import AppContainer


class CeleryScheduler:
    """
    Manages the Celery beat schedule with logging and performance tracking.
    """

    @inject
    def __init__(
        self,
        logger=Provide[AppContainer.struct_logger],
        tracker=Provide[AppContainer.performance_tracker],
    ):
        self.logger = logger
        self.tracker = tracker

    def initialize_schedule(self):
        """
        Define the Celery beat schedule dynamically.
        """
        with self.tracker.track_execution("Initialize Celery Beat Schedule"):
            try:
                self.logger.info("Starting Celery Beat Schedule initialization...")

                now = pendulum.now()
                self.logger.info(f"Current time for reference: {now.to_iso8601_string()}")

                schedule = {
                    "cleanup_old_data": {
                        "task": "celery.cleanup_tasks.cleanup_old_data",
                        "schedule": crontab(hour=3, minute=0),  # Runs daily at 3 AM
                    },
                    "download_example_video": {
                        "task": "celery.download_tasks.download_video",
                        "schedule": crontab(minute=0, hour="*/6"),  # Every 6 hours
                        "args": ["https://example.com/video-url"],
                    },
                    "log_current_time": {
                        "task": "celery.log_tasks.log_time",
                        "schedule": crontab(minute=0, hour="*"),  # Every hour
                        "args": [now.to_iso8601_string()],
                    },
                }

                self.logger.info("Celery Beat Schedule successfully initialized.")
                return schedule

            except Exception as e:
                self.logger.error(f"Failed to initialize Celery Beat Schedule: {e}")
                raise


# Automatically wire dependencies from AppContainer
AppContainer.wire(modules=[__name__])

# Instantiate the scheduler and initialize the Celery beat schedule
celery_scheduler = CeleryScheduler()
CELERY_BEAT_SCHEDULE = celery_scheduler.initialize_schedule()
