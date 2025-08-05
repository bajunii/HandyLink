from django.shortcuts import get_object_or_404
from rest_framework import status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import (
    ListAPIView, CreateAPIView, RetrieveAPIView, 
    UpdateAPIView, DestroyAPIView, GenericAPIView
)
from rest_framework.viewsets import ModelViewSet
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Job, JobCategory, JobApplication, JobReview, JobMessage
from .serializers import (
    JobSerializer, JobListSerializer, JobCreateSerializer, JobCategorySerializer,
    JobApplicationSerializer, ApplyToJobSerializer, JobReviewSerializer,
    JobMessageSerializer
)

class JobCategoryViewSet(ModelViewSet):
    """
    ViewSet for managing job categories
    """
    queryset = JobCategory.objects.filter(is_active=True)
    serializer_class = JobCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    @swagger_auto_schema(
        operation_summary='List all job categories',
        operation_description='Returns a list of all active job categories with job counts.',
        tags=['Job Categories']
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class JobListCreateView(GenericAPIView):
    """
    List jobs or create a new job
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    def get_queryset(self):
        return Job.objects.filter(status='open').select_related('posted_by', 'category', 'assigned_to')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return JobCreateSerializer
        return JobListSerializer
    
    @swagger_auto_schema(
        operation_summary='List available jobs',
        operation_description="""
        Returns a paginated list of open jobs with filtering and search capabilities.
        
        **Filters:**
        - category: Filter by job category ID
        - urgency: Filter by urgency level (low, medium, high, urgent)
        - is_remote: Filter remote jobs (true/false)
        
        **Search:** Search in title, description, and location
        **Ordering:** Sort by created_at, budget_min, or deadline
        """,
        tags=['Jobs']
    )
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_summary='Create a new job',
        operation_description='Create a new job posting. User must be authenticated.',
        request_body=JobCreateSerializer,
        responses={
            201: openapi.Response('Job created successfully', JobSerializer),
            400: 'Validation errors',
            401: 'Authentication required'
        },
        tags=['Jobs']
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            job = serializer.save()
            response_serializer = JobSerializer(job)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class JobDetailView(RetrieveAPIView):
    """
    Get detailed information about a specific job
    """
    queryset = Job.objects.select_related('posted_by', 'category', 'assigned_to')
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    @swagger_auto_schema(
        operation_summary='Get job details',
        operation_description='Returns detailed information about a specific job including applications.',
        tags=['Jobs']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class MyJobsView(ListAPIView):
    """
    List jobs posted by the authenticated user
    """
    serializer_class = JobListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'status']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Job.objects.filter(posted_by=self.request.user).select_related('category', 'assigned_to')
    
    @swagger_auto_schema(
        operation_summary='Get my posted jobs',
        operation_description='Returns all jobs posted by the authenticated user.',
        tags=['Jobs']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class JobApplicationView(GenericAPIView):
    """
    Apply to a job or manage job applications
    """
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ApplyToJobSerializer
        return JobApplicationSerializer
    
    @swagger_auto_schema(
        operation_summary='Apply to a job',
        operation_description='Submit an application for a specific job. User must be a verified provider.',
        request_body=ApplyToJobSerializer,
        responses={
            201: 'Application submitted successfully',
            400: 'Validation errors or already applied',
            403: 'Not a verified provider',
            404: 'Job not found'
        },
        tags=['Job Applications']
    )
    def post(self, request, job_id):
        job = get_object_or_404(Job, id=job_id, status='open')
        
        # Check if user is a verified provider
        if not hasattr(request.user, 'provider_profile'):
            return Response({
                'error': 'You must be a registered provider to apply for jobs.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        provider = request.user.provider_profile
        if not provider.is_verified or provider.status != 'approved':
            return Response({
                'error': 'Your provider account must be verified and approved.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Check if already applied
        if JobApplication.objects.filter(job=job, provider=provider).exists():
            return Response({
                'error': 'You have already applied for this job.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data, context={
            'request': request,
            'job': job
        })
        if serializer.is_valid(raise_exception=True):
            application = serializer.save()
            response_serializer = JobApplicationSerializer(application)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class JobApplicationListView(ListAPIView):
    """
    List applications for a specific job (job owner only)
    """
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        job_id = self.kwargs['job_id']
        job = get_object_or_404(Job, id=job_id, posted_by=self.request.user)
        return JobApplication.objects.filter(job=job).select_related('provider', 'provider__user')
    
    @swagger_auto_schema(
        operation_summary='Get job applications',
        operation_description='Returns all applications for a specific job. Only job owner can access.',
        tags=['Job Applications']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class AcceptApplicationView(GenericAPIView):
    """
    Accept a job application
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary='Accept job application',
        operation_description='Accept a specific application and assign the job to the provider.',
        responses={
            200: 'Application accepted successfully',
            403: 'Not authorized or job already assigned',
            404: 'Application not found'
        },
        tags=['Job Applications']
    )
    def post(self, request, application_id):
        application = get_object_or_404(
            JobApplication, 
            id=application_id, 
            job__posted_by=request.user,
            status='pending'
        )
        
        job = application.job
        if job.status != 'open':
            return Response({
                'error': 'This job is no longer open for applications.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Accept the application and assign the job
        application.status = 'accepted'
        application.save()
        
        job.assigned_to = application.provider
        job.status = 'in_progress'
        job.save()
        
        # Reject other pending applications
        JobApplication.objects.filter(
            job=job, 
            status='pending'
        ).exclude(id=application.id).update(status='rejected')
        
        return Response({
            'message': 'Application accepted successfully.',
            'job_status': job.status,
            'assigned_provider': application.provider.business_name
        })

class JobReviewView(CreateAPIView):
    """
    Create a review for a completed job
    """
    serializer_class = JobReviewSerializer
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary='Review a completed job',
        operation_description='Submit a review for a completed job. Only job owner can review.',
        tags=['Job Reviews']
    )
    def post(self, request, job_id):
        job = get_object_or_404(
            Job, 
            id=job_id, 
            posted_by=request.user, 
            status='completed'
        )
        
        if hasattr(job, 'review'):
            return Response({
                'error': 'This job has already been reviewed.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(
                job=job,
                reviewer=request.user,
                provider=job.assigned_to
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class UpdateJobStatusView(GenericAPIView):
    """
    Update job status (for job owner and assigned provider)
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary='Update job status',
        operation_description='Update the status of a job. Different users can perform different status updates.',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['in_progress', 'completed', 'cancelled'],
                    description='New status for the job'
                )
            },
            required=['status']
        ),
        tags=['Jobs']
    )
    def patch(self, request, job_id):
        job = get_object_or_404(Job, id=job_id)
        new_status = request.data.get('status')
        
        # Check permissions
        is_job_owner = job.posted_by == request.user
        is_assigned_provider = (
            hasattr(request.user, 'provider_profile') and 
            job.assigned_to == request.user.provider_profile
        )
        
        if not (is_job_owner or is_assigned_provider):
            return Response({
                'error': 'You are not authorized to update this job.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Validate status transitions
        valid_transitions = {
            'in_progress': ['completed'] if is_assigned_provider else ['cancelled'],
            'open': ['cancelled'] if is_job_owner else [],
            'completed': [],
            'cancelled': []
        }
        
        if new_status not in valid_transitions.get(job.status, []):
            return Response({
                'error': f'Cannot change status from {job.status} to {new_status}.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        job.status = new_status
        job.save()
        
        return Response({
            'message': f'Job status updated to {new_status}.',
            'status': job.status
        })
