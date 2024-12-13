"""API views for Job model."""

from rest_framework.viewsets import ModelViewSet
from rest_framework import authentication, permissions
from rest_framework.response import Response

from core.models import Job, User
from job.serializers import JobSerializers, JobDetailSerializer


class JobAPIViewSets(ModelViewSet):
    """API view for CRUD on Job."""
    queryset = Job.objects.all()
    serializer_class = JobDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        queryset = self.queryset.filter(status='OP')

        # Filter by job type (Full / Part time, Contractual)
        type = self.request.query_params.get('type')

        # Filter by user favorable job
        user_id = self.request.query_params.get('user')
        if user_id:
            job_category_id = User.objects.get(id=user_id).job_category

            if job_category_id:
                queryset = queryset.filter(job_category=job_category_id)

        if type:
            queryset = queryset.filter(type=type.upper())

        return queryset

    def perform_create(self, serializer):
        serializer.save(poster_id=self.request.user)

    def update(self,request, *args, **kwargs):
        partial = request.method == 'PATCH'
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'list':
            return JobSerializers
        return self.serializer_class
