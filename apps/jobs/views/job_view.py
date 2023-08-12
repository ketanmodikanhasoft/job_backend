from django.shortcuts import render
from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated

from apps.jobs.models import Jobs
from apps.jobs.serializers.job_serializer import JobSerializer


# JOB LIST VIEW #
class JobListAPIView(generics.ListAPIView):
    ## uncomment this for enable api authentication ##
    # permission_classes = [IsAuthenticated]
    serializer_class = JobSerializer  # seriazlier of JOB
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]  # for order and filter operations
    ordering_fields = [
        "job_id",
        "title",
        "description",
        "job_link",
        "location",
        "source",
        "company",
        "last_updated",
    ]  # fields for ordering
    search_fields = [
        "job_id",
        "title",
        "description",
        "job_link",
        "location",
        "source",
        "company",
        "last_updated",
    ]  # fields for filter

    def get_queryset(self):
        return Jobs.objects.all()
