from django.db import models

from apps.common.models import TimeStampModel

# Create your models here.


class Jobs(TimeStampModel):
    job_id = models.BigIntegerField()
    title = models.CharField(max_length=250)
    description = models.TextField()
    job_link = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=250, null=True, blank=True)
    source = models.CharField(max_length=250, null=True, blank=True)
    company = models.CharField(max_length=200, null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        get_latest_by = ("-id",)  ## for default descending order
