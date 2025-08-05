from django.urls import path
from .views import (
    CreateReviewView,
    ProviderReviewsView,
    MyReviewsView,
    ProviderRespondToReviewView,
    ReviewHelpfulnessView,
    ReviewDetailView
)

urlpatterns = [
    path('jobs/<int:job_id>/review/', CreateReviewView.as_view(), name='create-review'),
    path('providers/<int:provider_id>/reviews/', ProviderReviewsView.as_view(), name='provider-reviews'),
    path('my-reviews/', MyReviewsView.as_view(), name='my-reviews'),
    path('reviews/<int:review_id>/', ReviewDetailView.as_view(), name='review-detail'),
    path('reviews/<int:review_id>/respond/', ProviderRespondToReviewView.as_view(), name='respond-to-review'),
    path('reviews/<int:review_id>/helpful/', ReviewHelpfulnessView.as_view(), name='review-helpfulness'),
]
