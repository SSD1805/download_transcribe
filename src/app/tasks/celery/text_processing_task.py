from src.app.tasks.base_task import BaseTask
from dependency_injector.wiring import Provide, inject
from src.infrastructure.app.app_container import AppContainer


class TextProcessingTask(BaseTask):
    @inject
    def __init__(
        self,
        pipeline=Provide[AppContainer.text_processing_pipeline],
        logger_observer=Provide[AppContainer.logger_observer],
    ):
        super().__init__()
        self.pipeline = pipeline
        self.add_observer(logger_observer)

    def process(self, text_file: str, output_dir: str):
        self.logger.info(f"Processing text file: {text_file}")
        return self.pipeline.run(text_file, output_dir)


@app.task
def text_processing_pipeline_task(text_file: str, output_dir: str):
    task = Provide[AppContainer.text_processing_task]
    return task.execute(task.process, text_file, output_dir)
