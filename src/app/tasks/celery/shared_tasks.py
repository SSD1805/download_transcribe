from celery_app import shared_task
from dependency_injector.wiring import inject, Provide
from infrastructure.dependency_setup import container

@shared_task
@inject
def update_task_status(
    task_id: str,
    status: str,
    logger=Provide[container.logger],
    performance_tracker=Provide[container.performance_tracker]
):
    """
    Shared task to update task status.

    Args:
        task_id (str): The ID of the task.
        status (str): The new status to set.
        logger: Logger instance for logging (injected).
        performance_tracker: Performance tracker instance for tracking execution (injected).
    """
    try:
        with performance_tracker.track_execution(f"Update Task Status {task_id}"):
            logger.info(f"Updating status of task {task_id} to {status}.")
            # Placeholder for database update logic
            # db.update_task_status(task_id, status)
    except Exception as e:
        logger.error(f"Failed to update status for task {task_id}: {e}")
