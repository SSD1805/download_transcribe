# celery/schedule.py

from src.celery_tasks.schedule import CELERY_BEAT_SCHEDULE

CELERY_BEAT_SCHEDULE = {
    'cleanup_old_data': {
        'task': 'celery.cleanup_tasks.cleanup_old_data',
        'schedule': crontab(hour=3, minute=0),  # Runs daily at 3 AM
    },
    'download_example_video': {
        'task': 'celery.download_tasks.download_video',
        'schedule': crontab(minute=0, hour='*/6'),  # Every 6 hours
        'args': ['https://example.com/video-url']  # Sample URL for scheduled download
    }
}
