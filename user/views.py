"""Views for User API."""

from rest_framework import generics

from user.serializers import UserSerializers


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializers

