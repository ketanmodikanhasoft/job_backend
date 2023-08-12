import json

import requests
from bulk_sync import bulk_sync
from django.conf import settings

from apps.jobs.models import Jobs
from jobtask.celery import app


# THIS FUNCTION IS FOR FETCH JOBS #
@app.task(name="get_jobs")
def get_jobs():
    job_objects = []

    # PAYLOAD FOR GET JOBS #
    payload = {"keywords": "it", "location": "europe"}
    response = requests.post(
        settings.JOB_API,
        data=json.dumps(payload),
    )

    # CHECK IF RECEIVING SUCCESS RESPONSE #
    if response.ok:
        job_response = response.json()
        for job_details in job_response.get("jobs"):
            # EXTRACT DATA #
            job = Jobs()
            job.job_id = abs(job_details.get("id"))
            job.title = job_details.get("title")
            job.description = job_details.get("snippet")
            job.job_link = job_details.get("link")
            job.location = job_details.get("location")
            job.source = job_details.get("source")
            job.company = job_details.get("company")
            job.last_updated = job_details.get("updated")

            # APPEND DATA IN LIST FOR BULK OPERATIONS #
            job_objects.append(job)

    # KEY FIELD IS USED AS A WHERE CONDITION FOR DATA UPDATE #
    # BATCH SIZE IS USED FOR INSERT OR UPDATE ONLY THAT NUMBER OF RECORDS IN DATABASE #
    # SKIP_DELETES IS USED FOR SKIP DELETE IF OLD RECORDS NOT AVAILABLE IN NEW OBJECTS #
    key_fields = ["job_id"]
    if job_objects:
        bulk_sync(
            new_models=job_objects,
            filters=None,
            batch_size=200,
            key_fields=key_fields,
            fields=None,
            skip_deletes=True,
        )
