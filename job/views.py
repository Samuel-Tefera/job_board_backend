"""API views for Job model."""

from rest_framework.viewsets import ModelViewSet
from rest_framework import authentication, permissions, generics
from rest_framework.response import Response

from django.db.models import Count, Q, Prefetch

from core.models import Job, User, Application
from job.serializers import JobSerializer, JobDetailSerializer, JobFinderJobsSerializer
from application.serializers import ApplicationSerializers

class JobAPIViewSets(ModelViewSet):
    """API view for CRUD on Job."""
    queryset = Job.objects.all()
    serializer_class = JobDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        queryset = self.queryset.filter(status='OP').order_by('-created_at')

        # Search for a specific job
        search_query = self.request.query_params.get('search')
        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query))

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
            return JobSerializer
        return self.serializer_class


class JobPosterMyJobsView(generics.ListAPIView):
    """API view for job posters to view their jobs with applicants and counts"""
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        return Job.objects.filter(poster_id=self.request.user).annotate(applicant_count=Count('applications')).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        #Get the job
        jobs = self.get_queryset()

        data = []
        for job in jobs:
            job_data = JobDetailSerializer(job).data
            applicants = Application.objects.filter(job=job).select_related('applicant')
            applicants_data = ApplicationSerializers(applicants, many=True).data

            job_data['total_applicants'] = job.applicant_count
            job_data['applicants'] = applicants_data

            data.append(job_data)

        return Response(data)


class JobFinderMyJobsView(generics.ListAPIView):
    """
    API view for job finder to view jobs they applied for
    along with thier application status
    """
    serializer_class = JobFinderJobsSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        user = self.request.user
        user_application = Application.objects.filter(applicant=user).select_related('job')
        queryset = Job.objects.filter(
            applications__applicant=user
        ).prefetch_related(
            Prefetch('applications', queryset=user_application, to_attr='prefetched_applications')
        ).order_by('-created_at')

        return queryset
