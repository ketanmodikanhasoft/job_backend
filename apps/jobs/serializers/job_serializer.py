from rest_framework import serializers

from ..models import Jobs


# seriazlier for jobs #
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = "__all__"
        depth = 1
        extra_kwargs = {
            "id": {"read_only": True},
        }
