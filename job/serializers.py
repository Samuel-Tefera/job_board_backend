"""Job models serializers."""

from rest_framework import serializers

from core.models import Job
from application.serializers import ApplicationSerializers


class JobSerializers(serializers.ModelSerializer):
    """Serializers for Job model."""
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'type', 'job_category',
            'location', 'salary_range', 'created_at'
        ]
        read_only_fields = ['id']


    def create(self, validated_data):
        """Create a Job"""
        job = Job.objects.create(**validated_data)
        return job

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class JobDetailSerializer(serializers.ModelSerializer):
    """Serializer for Job detail."""

    class Meta:
        model=Job
        fields = JobSerializers.Meta.fields + ['status', 'poster_id', 'updated_at']


class JobFinderJobsSerializer(serializers.ModelSerializer):
    """Serializer for my jobs view of job finder"""
    applications = ApplicationSerializers(many=True)

    class Meta:
        model = Job
        fields = JobSerializers.Meta.fields + ['applications']
