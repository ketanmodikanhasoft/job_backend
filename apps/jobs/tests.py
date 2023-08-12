import json
import unittest
from unittest.mock import Mock, patch

import requests
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.jobs.models import Jobs
from apps.jobs.serializers.job_serializer import JobSerializer
from apps.jobs.tasks import get_jobs


class TestGetJobs(unittest.TestCase):
    # TEST CASE FOR WHEN API RESPONSE SEND EMPTY DATA #
    @patch("requests.post")
    def test_get_jobs_empty_data(self, mock_post):
        # CREATE MOCK TO AVOID ACTUAL API CALLS #
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {"jobs": []}
        mock_post.return_value = mock_response

        # First clear the database#
        Jobs.objects.filter().delete()
        # FETCH THE DATA  #
        get_jobs()

        # CHECK DATA COUNT IN DATABASE #
        self.assertEqual(Jobs.objects.all().count, 0)

    ## TEST CASE FOR GET JOBS WITH DATA  ##
    @patch("requests.post")
    def test_get_jobs_success(self, mock_post):
        # CREATE MOCK TO AVOID ACTUAL API CALLS #
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {
            "jobs": [
                {
                    "id": 1,
                    "title": "Job Title 1",
                    "snippet": "Job description snippet",
                    "link": "http://example.com/job/1",
                    "location": "Europe",
                    "source": "Example Source",
                    "company": "Example Company",
                    "updated": "2023-08-12T12:00:00Z",
                },
                # Add more job details as needed
            ]
        }
        mock_post.return_value = mock_response

        # FETCH THE DATA  #
        get_jobs()

        job = Jobs.objects.last()

        self.assertEqual(len(Jobs.objects.all()), 1)
        self.assertEqual(job.job_id, 1)
        self.assertEqual(job.title, "Job Title 1")
        self.assertEqual(job.description, "Job description snippet")
        self.assertEqual(job.job_link, "http://example.com/job/1")
        self.assertEqual(job.location, "Europe")
        self.assertEqual(job.source, "Example Source")
        self.assertEqual(job.company, "Example Company")


## TEST CASE FOR API ENDPOINT ##
class JobListAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("job-list")

        # Create some sample Job objects for testing
        Jobs.objects.create(
            title="Job 1",
            description="Description for Job 1",
            location="Location 1",
            company="Company 1",
            job_id=123,
        )
        Jobs.objects.create(
            title="Job 2",
            description="Description for Job 2",
            location="Location 2",
            company="Company 2",
            job_id=456,
        )

    # CREATED THIS FUNCTION TO MATCH SERIALIZER DATA AND API RESPONSE DATA #
    def assert_paginated_response_data_equal_serializer_data(
        self, response_data, serializer_data
    ):
        self.assertEqual(response_data["count"], len(serializer_data))
        for response_item, serializer_item in zip(
            response_data["results"], serializer_data
        ):
            self.assertEqual(response_item["id"], serializer_item["id"])
            self.assertEqual(response_item["title"], serializer_item["title"])
            self.assertEqual(response_item["job_id"], serializer_item["job_id"])

    ## GET ALL JOBS ##
    def test_list_jobs(self):
        response = self.client.get(self.url)
        jobs = Jobs.objects.all()
        serializer = JobSerializer(jobs, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_paginated_response_data_equal_serializer_data(
            response.data, serializer.data
        )

    ## FILTER OPERATION ON API ##
    def test_filter_by_title(self):
        response = self.client.get(self.url, {"search": "Job 1"})
        jobs = Jobs.objects.filter(title="Job 1")
        serializer = JobSerializer(jobs, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_paginated_response_data_equal_serializer_data(
            response.data, serializer.data
        )

    ## ORDERING OPERATION ON API ##
    def test_ordering_by_job_id(self):
        response = self.client.get(self.url, {"ordering": "job_id"})
        jobs = Jobs.objects.all().order_by("job_id")
        serializer = JobSerializer(jobs, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_paginated_response_data_equal_serializer_data(
            response.data, serializer.data
        )
