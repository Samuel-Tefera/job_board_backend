"""API views for application model."""

from rest_framework import generics, permissions, authentication
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import Application
from .serializers import ApplicationSerializers, UpdateApplicationStatus


class ApplicationCreateView(generics.CreateAPIView):
    """API view for create application."""
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user)


class ApplicationDetailView(generics.RetrieveAPIView):
    """API view for detail application."""
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]


class JobApplicationsListView(generics.ListAPIView):
    """API view for job applications list"""
    serializer_class = ApplicationSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        job_id = self.kwargs.get('job_id')
        return Application.objects.filter(job=job_id)


class ApplicationUpdateStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def patch(self, request, pk):
        application = Application.objects.get(id=pk)
        if application.job.poster_id != request.user:
            return Response({'error' :
                'Not authorized to update this application.'}, status=403)

        serializer = UpdateApplicationStatus(application, data=request.data, partail=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
