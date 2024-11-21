from celery import Celery
from .observable_task import ObservableTask
from .observers import LoggerObserver
from dependency_injector.wiring import inject, Provide
from infrastructure.app_container import AppContainer

app = Celery('tasks', broker='pyamqp://guest@localhost//')


class ObservableCeleryTask(ObservableTask):
    def __init__(self):
        super().__init__()


@app.task(bind=True)
@inject
def transcribe_audio(self, audio_file: str, logger_observer=Provide[AppContainer.logger_observer], *args, **kwargs):
    observable_task = ObservableCeleryTask()

    # Add observers
    observable_task.add_observer(logger_observer.update)

    try:
        observable_task.notify_observers('task_started', {"task_id": self.request.id, "audio_file": audio_file})

        # Task logic here - e.g., transcribe the audio file
        result = f"Transcribed content from {audio_file}"  # Placeholder for actual transcription logic

        observable_task.notify_observers('task_completed', {"task_id": self.request.id, "result": result})
        return result
    except Exception as e:
        observable_task.notify_observers('task_failed', {"task_id": self.request.id, "error": str(e)})
        raise e
