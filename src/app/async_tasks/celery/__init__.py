from celery_app import Celery

from django.conf import settings

# Initialize Celery
celery_app = Celery("project_name")

# Load settings from Django’s configuration
celery_app.config_from_object("django.conf:settings", namespace="CELERY")

# Discover async_tasks within each Django app
celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# Optional: Specify a custom default for the worker name
@celery_app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
