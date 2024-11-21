from celery import Celery
from .observable_task import ObservableTask
from .observers import LoggerObserver, TaskCoordinatorObserver
from dependency_injector.wiring import inject, Provide
from infrastructure.app_container import AppContainer

app = Celery('tasks', broker='pyamqp://guest@localhost//')


class ObservableCeleryTask(ObservableTask):
    def __init__(self):
        super().__init__()


@app.task(bind=True)
@inject
def download_file(self, file_url: str, logger_observer=Provide[AppContainer.logger_observer], *args, **kwargs):
    observable_task = ObservableCeleryTask()

    # Add observers
    coordinator_observer = TaskCoordinatorObserver()
    observable_task.add_observer(logger_observer.update)
    observable_task.add_observer(coordinator_observer.update)

    try:
        observable_task.notify_observers('task_started', {"task_id": self.request.id, "file_url": file_url})

        # Task logic here - e.g., download the file
        result = f"Downloaded content from {file_url}"  # Placeholder for actual download logic

        observable_task.notify_observers('task_completed', {"task_id": self.request.id, "result": result})
        return result
    except Exception as e:
        observable_task.notify_observers('task_failed', {"task_id": self.request.id, "error": str(e)})
        raise e
