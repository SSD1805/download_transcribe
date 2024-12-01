from dependency_injector.wiring import Provide, inject

from src.app.async_tasks.base_task import BaseTask
from src.infrastructure.app.app_container import AppContainer


class AudioProcessingTask(BaseTask):
    @inject
    def __init__(
        self,
        pipeline=Provide[AppContainer.audio_processing_pipeline],
        logger_observer=Provide[AppContainer.logger_observer],
    ):
        super().__init__()
        self.pipeline = pipeline
        self.add_observer(logger_observer)

    def process(self, input_file: str, output_dir: str):
        self.logger.info(f"Starting audio processing for {input_file}")
        try:
            return self.pipeline.run(input_file, output_dir)
        except Exception as e:
            self.logger.error(f"Audio processing failed for {input_file}: {e}")
            raise


@app.task(bind=True, max_retries=3)
def audio_processing_pipeline_task(self, input_file: str, output_dir: str):
    task = Provide[AppContainer.audio_processing_task]
    try:
        return task.execute(task.process, input_file, output_dir)
    except Exception as e:
        raise self.retry(exc=e, countdown=2**self.request.retries)
