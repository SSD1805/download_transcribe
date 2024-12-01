from dependency_injector.wiring import Provide, inject

from src.app.async_tasks.base_task import BaseTask
from src.infrastructure.app.app_container import AppContainer


class DownloadTask(BaseTask):
    @inject
    def __init__(
        self,
        pipeline=Provide[AppContainer.download_pipeline],
        logger_observer=Provide[AppContainer.logger_observer],
    ):
        super().__init__()
        self.pipeline = pipeline
        self.add_observer(logger_observer)

    def process(self, url: str, destination: str):
        self.logger.info(f"Downloading from {url}")
        return self.pipeline.download(url, destination)


@app.task
def download_pipeline_task(url: str, destination: str):
    task = Provide[AppContainer.download_task]
    return task.execute(task.process, url, destination)
