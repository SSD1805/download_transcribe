from dask.distributed import Client
from dependency_injector.wiring import Provide, inject

from src.infrastructure.app.app_container import AppContainer

# Set up Dask client
client = Client("localhost:8786")


@inject
def ner_task(
    text: str, logger_observer=Provide[AppContainer.logger_observer], *args, **kwargs
):
    observable_task = ObservableDaskTask()

    # Add observers
    observable_task.add_observer(logger_observer.update)

    try:
        observable_task.notify_observers("task_started", {"text_processing": text})

        # Task logic here - e.g., perform NER on the text_processing
        result = f"NER performed on text_processing: {text}"  # Placeholder for actual NER logic

        observable_task.notify_observers(
            "task_completed", {"text_processing": text, "result": result}
        )
        return result
    except Exception as e:
        observable_task.notify_observers("task_failed", {"text_processing": text, "error": str(e)})
        raise e


# Submit the task to Dask
future = client.submit(ner_task, "Sample text_processing for NER.")
