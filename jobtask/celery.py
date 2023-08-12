from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# setting the Django settings module.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jobtask.settings")
app = Celery("likelemba")
app.config_from_object("django.conf:settings", namespace="CELERY")

# Looks up for task modules in Django applications and loads them
app.autodiscover_tasks(settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    "get_jobs": {
        "task": "get_jobs",
        "schedule": crontab(
            minute="*/5", hour="*"
        ),  # CELERY TASK TO GET JOB DATA EVERY 5 MIN, WE CAN CHANGE THIS TIME AS PER REQUIREMENT
    }
}


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
