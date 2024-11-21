from dask.distributed import Client
from .observable_task import ObservableTask
from dependency_injector.wiring import inject, Provide
from infrastructure.app_container import AppContainer
from tasks.observers import LoggerObserver

# Set up Dask client
client = Client('localhost:8786')

@inject
def transcription_task(audio_file: str, logger_observer=Provide[AppContainer.logger_observer], *args, **kwargs):
    observable_task = ObservableDaskTask()

    # Add observers
    observable_task.add_observer(logger_observer.update)

    try:
        observable_task.notify_observers('task_started', {"audio_file": audio_file})

        # Task logic here - e.g., transcribe the audio file
        result = f"Transcribed content from {audio_file}"  # Placeholder for actual transcription logic

        observable_task.notify_observers('task_completed', {"audio_file": audio_file, "result": result})
        return result
    except Exception as e:
        observable_task.notify_observers('task_failed', {"audio_file": audio_file, "error": str(e)})
        raise e

# This worker can be submitted by the coordinator or another workflow step
