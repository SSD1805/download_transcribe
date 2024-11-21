from dask.distributed import Client
from .observable_task import ObservableTask
from dependency_injector.wiring import inject, Provide
from src.infrastructure import AppContainer
from tasks.observers import LoggerObserver

# Set up Dask client
client = Client('localhost:8786')

@inject
def ner_task(text: str, logger_observer=Provide[AppContainer.logger_observer], *args, **kwargs):
    observable_task = ObservableDaskTask()

    # Add observers
    observable_task.add_observer(logger_observer.update)

    try:
        observable_task.notify_observers('task_started', {"text": text})

        # Task logic here - e.g., perform NER on the text
        result = f"NER performed on text: {text}"  # Placeholder for actual NER logic

        observable_task.notify_observers('task_completed', {"text": text, "result": result})
        return result
    except Exception as e:
        observable_task.notify_observers('task_failed', {"text": text, "error": str(e)})
        raise e

# Submit the task to Dask
future = client.submit(ner_task, 'Sample text for NER.')
