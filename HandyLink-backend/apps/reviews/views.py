from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Avg, Count, Q
from django.utils import timezone
from datetime import timedelta

from .models import Review, ReviewHelpful, ReviewResponse
from .serializers import (
    ReviewCreateSerializer, ReviewSerializer, ReviewResponseSerializer
)
from apps.jobs.models import Job
from apps.providers.models import Provider

class CreateReviewView(GenericAPIView):
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary='Create a review for completed job',
        operation_description="""
        Allows users to create reviews for completed jobs.
        
        **Requirements:**
        - Job must be completed
        - User must be the job poster
        - Review hasn't been created yet
        """,
        responses={
            201: openapi.Response(description='Review created successfully'),
            400: openapi.Response(description='Validation errors'),
            404: openapi.Response(description='Job not found')
        },
        tags=['Reviews']
    )
    def post(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id, posted_by=request.user, status='completed')
            
            # Check if review already exists
            if hasattr(job, 'main_review'):
                return Response({
                    'message': 'Review already exists for this job'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if not job.assigned_to:
                return Response({
                    'message': 'No provider assigned to this job'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                review = serializer.save(
                    job=job,
                    reviewer=request.user,
                    provider=job.assigned_to
                )
                
                # Update provider's average rating
                self.update_provider_rating(job.assigned_to)
                
                return Response({
                    'message': 'Review created successfully',
                    'review_id': review.id
                }, status=status.HTTP_201_CREATED)
                
        except Job.DoesNotExist:
            return Response({
                'message': 'Job not found or not eligible for review'
            }, status=status.HTTP_404_NOT_FOUND)
    
    def update_provider_rating(self, provider):
        """Update provider's average rating based on all reviews"""
        reviews = provider.reviews_received.all()
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        total_reviews = reviews.count()
        
        provider.rating = avg_rating or 0.0
        provider.total_reviews = total_reviews
        provider.save()

class ProviderReviewsView(ListAPIView):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        provider_id = self.kwargs['provider_id']
        return Review.objects.filter(provider_id=provider_id).select_related(
            'reviewer', 'provider', 'job'
        )
    
    @swagger_auto_schema(
        operation_summary='Get provider reviews',
        operation_description='Returns all reviews for a specific provider.',
        tags=['Reviews']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class MyReviewsView(ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Review.objects.filter(reviewer=self.request.user).select_related(
            'provider', 'job'
        )
    
    @swagger_auto_schema(
        operation_summary='Get my reviews',
        operation_description='Returns all reviews written by the authenticated user.',
        tags=['Reviews']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ProviderRespondToReviewView(GenericAPIView):
    serializer_class = ReviewResponseSerializer
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary='Respond to a review',
        operation_description='Allows providers to respond to reviews.',
        tags=['Reviews']
    )
    def post(self, request, review_id):
        try:
            review = Review.objects.get(
                id=review_id,
                provider__user=request.user
            )
            
            if review.provider_response:
                return Response({
                    'message': 'Response already exists for this review'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Update the review directly instead of using separate model
            review.provider_response = request.data.get('content', '')
            review.response_date = timezone.now()
            review.save()
            
            return Response({
                'message': 'Response added successfully'
            }, status=status.HTTP_200_OK)
                
        except Review.DoesNotExist:
            return Response({
                'message': 'Review not found'
            }, status=status.HTTP_404_NOT_FOUND)

class ReviewHelpfulnessView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary='Mark review as helpful/not helpful',
        operation_description='Allows users to vote on review helpfulness.',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'is_helpful': openapi.Schema(type=openapi.TYPE_BOOLEAN)
            }
        ),
        tags=['Reviews']
    )
    def post(self, request, review_id):
        try:
            review = Review.objects.get(id=review_id)
            
            # Check if user already voted
            helpfulness, created = ReviewHelpful.objects.get_or_create(
                review=review,
                user=request.user,
                defaults={'is_helpful': request.data.get('is_helpful', True)}
            )
            
            if not created:
                # Update existing vote
                helpfulness.is_helpful = request.data.get('is_helpful', True)
                helpfulness.save()
            
            return Response({
                'message': 'Vote recorded successfully'
            }, status=status.HTTP_200_OK)
            
        except Review.DoesNotExist:
            return Response({
                'message': 'Review not found'
            }, status=status.HTTP_404_NOT_FOUND)

class ReviewDetailView(RetrieveAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    
    @swagger_auto_schema(
        operation_summary='Get review details',
        operation_description='Returns detailed information about a specific review.',
        tags=['Reviews']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
