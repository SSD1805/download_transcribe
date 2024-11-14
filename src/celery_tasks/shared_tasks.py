# celery_tasks/shared_tasks.py

from celery import shared_task
from src.core.logger_manager import LoggerManager

logger = LoggerManager().get_logger()


@shared_task
def update_task_status(task_id, status):
    """
    Shared task to update task status in the database.

    Args:
        task_id (str): The ID of the task.
        status (str): The new status to set.
    """
    # Update task status in the database or logging system
    logger.info(f"Updating status of task {task_id} to {status}.")
    # Example implementation to update status in database
