# celery_tasks/schedule.py

from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'cleanup_old_data': {
        'task': 'celery_tasks.cleanup_tasks.cleanup_old_data',
        'schedule': crontab(hour=3, minute=0),  # Runs daily at 3 AM
    },
    'download_example_video': {
        'task': 'celery_tasks.download_tasks.download_video',
        'schedule': crontab(minute=0, hour='*/6'),  # Every 6 hours
        'args': ['https://example.com/video-url']  # Sample URL for scheduled download
    }
}
