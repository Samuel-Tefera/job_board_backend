"""Serializers for User API View"""

from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers


class UserSerializers(serializers.ModelSerializer):
    """Serializers for user object."""
    class Meta:
        model = get_user_model()
        fields = [
            'first_name', 'last_name', 'email', 'gender',
            'user_type', 'bio', 'profile_pic_url', 'resume_url',
            'job_category', 'password'
        ]
        extra_kwargs = {'password' : {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
