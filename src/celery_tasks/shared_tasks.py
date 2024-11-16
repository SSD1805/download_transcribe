from celery import shared_task
from src.core.logger_manager import LoggerManager
from src.core.performance_tracker import PerformanceTracker

logger = LoggerManager().get_logger()
performance_tracker = PerformanceTracker()

@shared_task
def update_task_status(task_id, status):
    """
    Shared task to update task status in the database.

    Args:
        task_id (str): The ID of the task.
        status (str): The new status to set.
    """
    try:
        # Track the execution of the status update
        with performance_tracker.track_execution(f"Update Task Status {task_id}"):
            # Update task status in the database or logging system
            logger.info(f"Updating status of task {task_id} to {status}.")
            # Placeholder for database update
            # db.update_task_status(task_id, status)
    except Exception as e:
        logger.error(f"Failed to update status for task {task_id}: {e}")
