# src/app/tasks/observers/coordinator_observer.py
from dask.distributed import Client
from celery import Celery
from src.app.utils.application_logger import ApplicationLogger


class CoordinatorObserver:
    """
    Observer class that coordinates task transitions based on lifecycle events.
    """

    def __init__(self, logger=None, dask_client=None, celery_app=None):
        """
        Initializes the CoordinatorObserver.
        :param logger: Logger instance (defaults to ApplicationLogger).
        :param dask_client: Dask distributed client instance.
        :param celery_app: Celery app instance.
        """
        self.logger = logger or ApplicationLogger.get_logger()
        self.dask_client = dask_client or Client()
        self.celery_app = celery_app or Celery("tasks")

    def update(self, event: str, data: dict):
        """
        Handles task events and coordinates actions accordingly.
        :param event: Event type (e.g., 'task_completed', 'task_failed').
        :param data: Associated event data.
        """
        if event == "task_completed":
            self.handle_task_completed(data)
        elif event == "task_failed":
            self.handle_task_failed(data)
        else:
            self.logger.warning("Unknown event type", event=event, data=data)

    def handle_task_completed(self, data: dict):
        """
        Handles task completion events.
        :param data: Dictionary containing task metadata (e.g., output data).
        """
        self.logger.info("Handling task completion", **data)

        # Example: Trigger the transcription pipeline after audio processing
        if data.get("function") == "process_audio_file":
            output_file = data.get("result", {}).get("output_file")
            if output_file:
                self.logger.info(f"Starting transcription pipeline for {output_file}")
                self.celery_app.send_task(
                    "transcription_pipeline_task",
                    kwargs={"input_file": output_file, "output_dir": "/transcriptions"},
                )

    def handle_task_failed(self, data: dict):
        """
        Handles task failure events.
        :param data: Dictionary containing error information.
        """
        self.logger.error("Handling task failure", **data)

        # Example: Retry the failed task or log for manual intervention
        failed_task = data.get("function")
        error = data.get("error")
        self.logger.error(f"Task {failed_task} failed with error: {error}")
        # Optionally trigger a retry or notify a monitoring system

class CoordinatorObserver:
    def __init__(self, logger=None, celery_app=None):
        self.logger = logger or ApplicationLogger.get_logger()
        self.celery_app = celery_app or Celery("tasks")

    def update(self, event: str, data: dict):
        if event == "task_completed" and data.get("function") == "download_pipeline_task":
            downloaded_file = data.get("result", {}).get("downloaded_file")
            if downloaded_file:
                self.logger.info(f"Triggering audio pipeline for {downloaded_file}")
                self.celery_app.send_task(
                    "audio_processing_pipeline_task",
                    kwargs={"input_file": downloaded_file},
                )