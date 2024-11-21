from dask.distributed import Client
from .observable_task import ObservableTask
from dependency_injector.wiring import inject, Provide
from infrastructure.app_container import AppContainer
from tasks.observers import LoggerObserver

# Set up Dask client
client = Client('localhost:8786')

@inject
def text_segmentation_task(text: str, logger_observer=Provide[AppContainer.logger_observer], *args, **kwargs):
    observable_task = ObservableDaskTask()

    # Add observers
    observable_task.add_observer(logger_observer.update)

    try:
        observable_task.notify_observers('task_started', {"text": text})

        # Task logic here - e.g., segment the text
        result = f"Text segmented: {text}"  # Placeholder for actual segmentation logic

        observable_task.notify_observers('task_completed', {"text": text, "result": result})
        return result
    except Exception as e:
        observable_task.notify_observers('task_failed', {"text": text, "error": str(e)})
        raise e

# Submit the task to Dask
future = client.submit(text_segmentation_task, 'Sample text for segmentation.')

from tasks.observers import LoggerObserver, DaskCoordinatorObserver

@inject
def text_segmentation_task(text: str,
                           logger_observer=Provide[AppContainer.logger_observer],
                           coordinator_observer=Provide[AppContainer.dask_coordinator_observer],
                           *args, **kwargs):
    observable_task = ObservableDaskTask()

    # Add observers
    observable_task.add_observer(logger_observer.update)
    observable_task.add_observer(coordinator_observer.update)

    try:
        observable_task.notify_observers('task_started', {"text": text})

        # Task logic here - e.g., segment the text
        result = f"Text segmented: {text}"  # Placeholder for actual segmentation logic

        observable_task.notify_observers('task_completed', {"text": text, "result": result})
        return result
    except Exception as e:
        observable_task.notify_observers('task_failed', {"text": text, "error": str(e)})
        raise e

from dask.distributed import Client
from .observable_task import ObservableTask
from dependency_injector.wiring import inject, Provide
from infrastructure.app_container import AppContainer
from tasks.observers import LoggerObserver

# Set up Dask client
client = Client('localhost:8786')

@inject
def text_segmentation_task(text: str, logger_observer=Provide[AppContainer.logger_observer], *args, **kwargs):
    observable_task = ObservableDaskTask()

    # Add observers
    observable_task.add_observer(logger_observer.update)

    try:
        observable_task.notify_observers('task_started', {"text": text})

        # Task logic here - e.g., segment the text
        result = f"Text segmented: {text}"  # Placeholder for actual segmentation logic

        observable_task.notify_observers('task_completed', {"text": text, "result": result})
        return result
    except Exception as e:
        observable_task.notify_observers('task_failed', {"text": text, "error": str(e)})
        raise e

# Submit the task to Dask
future = client.submit(text_segmentation_task, 'Sample text for segmentation.')

from tasks.observers import LoggerObserver, DaskCoordinatorObserver

@inject
def text_segmentation_task(text: str,
                           logger_observer=Provide[AppContainer.logger_observer],
                           coordinator_observer=Provide[AppContainer.dask_coordinator_observer],
                           *args, **kwargs):
    observable_task = ObservableDaskTask()

    # Add observers
    observable_task.add_observer(logger_observer.update)
    observable_task.add_observer(coordinator_observer.update)

    try:
        observable_task.notify_observers('task_started', {"text": text})

        # Task logic here - e.g., segment the text
        result = f"Text segmented: {text}"  # Placeholder for actual segmentation logic

        observable_task.notify_observers('task_completed', {"text": text, "result": result})
        return result
    except Exception as e:
        observable_task.notify_observers('task_failed', {"text": text, "error": str(e)})
        raise e
