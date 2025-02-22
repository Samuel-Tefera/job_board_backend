"""Views for User API."""

from django.utils.timezone import now
from django.contrib.auth import get_user_model

from rest_framework import (
    generics,
    permissions,
    authentication
)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializers import (
    UserSerializers,
    AuthTokenSerializer
)


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializers


class UserLoginView(ObtainAuthToken):
    """Create a new auth token for validate user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = token.user

        user.last_login = now()
        user.save()

        return Response({
            'token' : token.key,
            'user_id' : user.pk,
            'email' : user.email,
        })


class UserLogoutView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({'message' : 'Successfully logged out'}, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=400)


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializers
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserDetailView(generics.RetrieveAPIView):
    """API view to retrieve a user's information by their ID."""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    lookup_field = 'id'
