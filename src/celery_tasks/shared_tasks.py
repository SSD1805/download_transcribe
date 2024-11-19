from celery import shared_task
from src.utils.structlog_logger import StructLogger
from src.utils.performance_tracker import PerformanceTracker

logger = StructLogger.get_logger()
perf_tracker = PerformanceTracker.get_instance()

@shared_task
def update_task_status(task_id, status):
    """
    Shared task to update task status.

    Args:
        task_id (str): The ID of the task.
        status (str): The new status to set.
    """
    try:
        with perf_tracker.track_execution(f"Update Task Status {task_id}"):
            logger.info(f"Updating status of task {task_id} to {status}.")
            # Placeholder for database update
            # db.update_task_status(task_id, status)
    except Exception as e:
        logger.error(f"Failed to update status for task {task_id}: {e}")
