from src.app.tasks.base_task import BaseTask
from dependency_injector.wiring import Provide, inject
from src.infrastructure.app.app_container import AppContainer


class TranscriptionTask(BaseTask):
    @inject
    def __init__(
        self,
        pipeline=Provide[AppContainer.transcription_pipeline],
        logger_observer=Provide[AppContainer.logger_observer],
    ):
        super().__init__()
        self.pipeline = pipeline
        self.add_observer(logger_observer)

    def process(self, audio_file: str, output_dir: str):
        self.logger.info(f"Transcribing audio file: {audio_file}")
        try:
            return self.pipeline.run(audio_file, output_dir)
        except Exception as e:
            self.logger.error(f"Transcription failed for {audio_file}: {e}")
            raise


@app.task(bind=True, max_retries=3)
def transcription_pipeline_task(self, audio_file: str, output_dir: str):
    task = Provide[AppContainer.transcription_task]
    try:
        return task.execute(task.process, audio_file, output_dir)
    except Exception as e:
        raise self.retry(exc=e, countdown=2**self.request.retries)
