from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    JobCategoryViewSet, JobListCreateView, JobDetailView, MyJobsView,
    JobApplicationView, JobApplicationListView, AcceptApplicationView,
    JobReviewView, UpdateJobStatusView
)

# Create router for viewsets
router = DefaultRouter()
router.register(r'categories', JobCategoryViewSet)

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
    
    # Job URLs
    path('jobs/', JobListCreateView.as_view(), name='job-list-create'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('jobs/<int:job_id>/status/', UpdateJobStatusView.as_view(), name='job-status-update'),
    path('my-jobs/', MyJobsView.as_view(), name='my-jobs'),
    
    # Job Application URLs
    path('jobs/<int:job_id>/apply/', JobApplicationView.as_view(), name='job-apply'),
    path('jobs/<int:job_id>/applications/', JobApplicationListView.as_view(), name='job-applications'),
    path('applications/<int:application_id>/accept/', AcceptApplicationView.as_view(), name='accept-application'),
    
    # Job Review URLs
    path('jobs/<int:job_id>/review/', JobReviewView.as_view(), name='job-review'),
]
