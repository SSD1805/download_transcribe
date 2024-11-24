# src/app/tasks/celery/download_task.py
from celery import Celery
from dependency_injector.wiring import Provide, inject
from src.infrastructure.app.app_container import AppContainer
from src.app.tasks.base_task import BaseTask

app = Celery("tasks", broker="redis://localhost:6379/0")


class DownloadTask(BaseTask):
    @inject
    def __init__(
        self,
        download_pipeline=Provide[AppContainer.download_pipeline],
        logger_observer=Provide[AppContainer.logger_observer],
        coordinator_observer=Provide[AppContainer.coordinator_observer],
    ):
        super().__init__()
        self.download_pipeline = download_pipeline
        self.add_observer(logger_observer)
        self.add_observer(coordinator_observer)

    def process(self, url: str, download_type: str):
        return self.download_pipeline.run(url, download_type=download_type)


@app.task
@inject
def download_pipeline_task(
    url: str,
    download_type: str = "video",
    download_task=Provide[AppContainer.download_task],
):
    return download_task.execute(download_task.process, url, download_type=download_type)
