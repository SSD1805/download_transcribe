from dask.distributed import Client
from .observable_task import ObservableTask
from dependency_injector.wiring import inject, Provide
from src.infrastructure import AppContainer
from tasks.observers import LoggerObserver

# Set up Dask client
client = Client("localhost:8786")


class ObservableDaskTask(ObservableTask):
    def __init__(self):
        super().__init__()


@inject
def audio_conversion_task(
    audio_file: str,
    logger_observer=Provide[AppContainer.logger_observer],
    *args,
    **kwargs,
):
    observable_task = ObservableDaskTask()

    # Add observers
    observable_task.add_observer(logger_observer.update)

    try:
        observable_task.notify_observers("task_started", {"audio_file": audio_file})

        # Task logic here - e.g., convert the audio file
        result = f"Converted {audio_file}"  # Placeholder for actual conversion logic

        observable_task.notify_observers(
            "task_completed", {"audio_file": audio_file, "result": result}
        )
        return result
    except Exception as e:
        observable_task.notify_observers(
            "task_failed", {"audio_file": audio_file, "error": str(e)}
        )
        raise e


# Submit the task to Dask
future = client.submit(audio_conversion_task, "sample_audio.wav")


@inject
def audio_conversion_task(
    audio_file: str,
    logger_observer=Provide[AppContainer.logger_observer],
    coordinator_observer=Provide[AppContainer.dask_coordinator_observer],
    *args,
    **kwargs,
):
    observable_task = ObservableDaskTask()

    # Add observers
    observable_task.add_observer(logger_observer.update)
    observable_task.add_observer(coordinator_observer.update)

    try:
        observable_task.notify_observers("task_started", {"audio_file": audio_file})

        # Task logic here - e.g., convert the audio file
        result = f"Converted {audio_file}"  # Placeholder for actual conversion logic

        observable_task.notify_observers(
            "task_completed", {"audio_file": audio_file, "result": result}
        )
        return result
    except Exception as e:
        observable_task.notify_observers(
            "task_failed", {"audio_file": audio_file, "error": str(e)}
        )
        raise e


@inject
def audio_conversion_task(
    audio_file: str,
    logger_observer=Provide[AppContainer.logger_observer],
    coordinator_observer=Provide[AppContainer.dask_coordinator_observer],
    *args,
    **kwargs,
):
    observable_task = ObservableDaskTask()

    # Add observers
    observable_task.add_observer(logger_observer.update)
    observable_task.add_observer(coordinator_observer.update)

    try:
        observable_task.notify_observers("task_started", {"audio_file": audio_file})

        # Task logic here - e.g., convert the audio file
        result = f"Converted {audio_file}"  # Placeholder for actual conversion logic

        observable_task.notify_observers(
            "task_completed", {"audio_file": audio_file, "result": result}
        )
        return result
    except Exception as e:
        observable_task.notify_observers(
            "task_failed", {"audio_file": audio_file, "error": str(e)}
        )
        raise e
