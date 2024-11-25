from celery import Celery
from dask.distributed import Client
from src.app.utils.application_logger import ApplicationLogger


class CoordinatorObserver:
    """
    Observer class that coordinates task transitions based on lifecycle events.
    """

    def __init__(self, logger=None, dask_client=None, celery_app=None):
        self.logger = logger or ApplicationLogger.get_logger()
        self.dask_client = dask_client or Client()
        self.celery_app = celery_app or Celery("tasks")

    def update(self, event: str, data: dict):
        if event == "task_completed":
            self.handle_task_completed(data)
        elif event == "task_failed":
            self.handle_task_failed(data)
        else:
            self.logger.warning(f"Unknown event type: {event}", extra=data)

    def handle_task_completed(self, data: dict):
        self.logger.info(f"Handling task completion for {data.get('function')}")
        if data.get("function") == "process_audio_file":
            output_file = data.get("result", {}).get("output_file")
            if output_file:
                self.celery_app.send_task(
                    "transcription_pipeline_task",
                    kwargs={"input_file": output_file, "output_dir": "/transcriptions"},
                )

    def handle_task_failed(self, data: dict):
        self.logger.error(f"Handling task failure for {data.get('function')}")
        # Add retry logic or external notification here.
