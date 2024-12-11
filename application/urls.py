"""URL mapping for job applications"""

from django.urls import path
from . import views

urlpatterns = [
    path('applications', views.ApplicationCreateView.as_view(),
         name='application-create'),
    path('applications/<int:pk>/', views.ApplicationDetailView.as_view(),
         name='application-detail'),
    path('applications/<int:pk>/update-status/', views.ApplicationUpdateStatusView.as_view(),
         name='application-update_status'),
    path('jobs/<int:jon_id>/applications/', views.JobApplicationsListView.as_view(),
         name='job-appications-list' )
]
