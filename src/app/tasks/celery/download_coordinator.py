from dependency_injector.wiring import inject, Provide
from infrastructure.app_container import AppContainer
from .transcription_tasks import transcribe_audio

class DownloadCoordinatorObserver:
    @inject
    def __init__(self, logger=Provide[AppContainer.struct_logger]):
        self.logger = logger

    def update(self, event: str, data: dict):
        if event == 'task_completed':
            self.logger.info(f"Download completed: {data}. Initiating transcription.")
            audio_file = data.get("result")
            # Trigger the transcription task with the completed download file.
            transcribe_audio.delay(audio_file)
        elif event == 'task_failed':
            self.logger.error(f"Download failed: {data}. No further actions will be taken.")

# Example usage:
# This coordinator observer can be added to any download task that we want to coordinate.
