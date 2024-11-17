# celery_tasks/__init__.py

from celery import Celery
from django.conf import settings

# Initialize Celery
celery_app = Celery('project_name')

# Load settings from Django’s configuration
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover tasks within each Django data and the celery_tasks folder
celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS + ['celery_tasks'])
