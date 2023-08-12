from django.urls import re_path

from apps.jobs.views.job_view import JobListAPIView

urlpatterns = [
    re_path(
        "list-jobs/",
        JobListAPIView.as_view(),
        name="job-list",
    )
]
