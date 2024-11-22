from dependency_injector.wiring import Provide, inject

from src.infrastructure.app.app_container import AppContainer


class LoggerObserver:
    @inject
    def __init__(self, logger=Provide[AppContainer.struct_logger]):
        self.logger = logger

    def update(self, event: str, data: dict) -> None:
        self.logger.info(f"Event: {event}, Data: {data}")


from dependency_injector.wiring import Provide, inject

from src.infrastructure.app.app_container import AppContainer

from .transcription_worker import (
    transcription_task,
)  # Assuming we need to coordinate with transcription


class DaskCoordinatorObserver:
    @inject
    def __init__(self, logger=Provide[AppContainer.struct_logger]):
        self.logger = logger

    def update(self, event: str, data: dict):
        if event == "task_completed":
            self.logger.info(
                f"Audio Conversion completed: {data}. Initiating transcription."
            )
            audio_file = data.get("audio_file")
            # Trigger the transcription task with the converted audio file.
            client = Client("localhost:8786")
            client.submit(transcription_task, audio_file)
        elif event == "task_failed":
            self.logger.error(
                f"Audio Conversion failed: {data}. Handling failure accordingly."
            )
            # Implement retry logic or error handling if needed


from dask.distributed import Client
from dependency_injector.wiring import Provide, inject

from src.infrastructure.app.app_container import AppContainer

from .ner_worker import ner_task


class DaskCoordinatorObserver:
    @inject
    def __init__(self, logger=Provide[AppContainer.struct_logger]):
        self.logger = logger

    def update(self, event: str, data: dict):
        if event == "task_completed":
            self.logger.info(f"Task completed: {data}")

            # Handle coordination based on the task type
            if "Text segmented" in data.get("result"):
                self.logger.info("Initiating NER task after text segmentation.")
                text = data.get("text")
                client = Client("localhost:8786")
                client.submit(ner_task, text)

        elif event == "task_failed":
            self.logger.error(f"Task failed: {data}. Handling failure accordingly.")
            # Implement retry logic or error handling if needed
