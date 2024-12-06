"""URL mapping for Job API"""

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('job', views.JobAPIViewSets)

app_name = 'job'

urlpatterns = [
    path('', include(router.urls))
]
