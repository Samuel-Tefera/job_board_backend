"""URL mapping for Job API"""

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('jobs', views.JobAPIViewSets)

app_name = 'job'

urlpatterns = [
    path('', include(router.urls)),
    path('my-jobs/posted/', view=views.JobPosterMyJobsView.as_view(), name='poster-jobs'),
    path('my-jobs/applied/', view=views.JobFinderMyJobsView.as_view(), name='finder-jobs'),
]
