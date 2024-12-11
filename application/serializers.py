"""A serializer for application model"""

from rest_framework import serializers

from core.models import Application


class ApplicationSerializers(serializers.ModelSerializer):
    """Application Serilalizer"""
    class Meta:
        model = Application
        fields = ['id', 'job', 'applicant', 'status', 'created_at', 'updated_at']
        read_only_fileds = ['id', 'created_at', 'updated_at', 'status']


class UpdateApplicationStatus(serializers.ModelSerializer):
    """Serielizer to update status of application"""
    class Meta:
        model = Application
        fields = ['status']
        extra_kwargs = {
            'status' : {'required' : True, 'choice' : ['acp', 'rej']}
        }
