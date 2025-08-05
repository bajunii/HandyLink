from django.db import models
from django.contrib.auth import get_user_model
from apps.providers.models import Provider
from apps.jobs.models import Job

User = get_user_model()

class Review(models.Model):
    # Core relationships - using different related_name to avoid conflicts
    job = models.OneToOneField(Job, on_delete=models.CASCADE, related_name='main_review')  # Changed related_name
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_written')
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='reviews_received')
    
    # Review content
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    title = models.CharField(max_length=255)
    content = models.TextField()
    
    # Detailed ratings
    quality_rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    timeliness_rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    communication_rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    value_rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    
    # Additional features
    is_verified = models.BooleanField(default=True)
    photos = models.JSONField(default=list, blank=True)
    would_recommend = models.BooleanField(default=True)
    
    # Provider response
    provider_response = models.TextField(blank=True)
    response_date = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review for {self.job.title} - {self.rating} stars"

    @property
    def average_detailed_rating(self):
        return (
            self.quality_rating + 
            self.timeliness_rating + 
            self.communication_rating + 
            self.value_rating
        ) / 4

class ReviewResponse(models.Model):
    review = models.OneToOneField(Review, on_delete=models.CASCADE, related_name='response')
    responder = models.ForeignKey(User, on_delete=models.CASCADE)  # Usually the provider
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response to review for {self.review.job.title}"

class ReviewHelpful(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='helpful_votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_helpful = models.BooleanField()  # True for helpful, False for not helpful
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['review', 'user']

    def __str__(self):
        return f"{'Helpful' if self.is_helpful else 'Not helpful'} vote for review {self.review.id}"
