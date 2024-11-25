from dependency_injector.wiring import Provide, inject

from src.app.tasks.base_task import BaseTask
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
        return self.pipeline.run(input_file, output_dir)


@app.task
def audio_processing_pipeline_task(input_file: str, output_dir: str):
    task = Provide[AppContainer.audio_processing_task]
    return task.execute(task.process, input_file, output_dir)
