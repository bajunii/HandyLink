from rest_framework import serializers
from .models import Review, ReviewResponse, ReviewHelpful
from apps.jobs.models import Job

class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'title', 'content', 'rating', 'quality_rating', 
            'timeliness_rating', 'communication_rating', 'value_rating',
            'would_recommend', 'photos'
        ]
    
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value

class ReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.SerializerMethodField()
    provider_name = serializers.CharField(source='provider.business_name', read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)
    helpful_votes = serializers.SerializerMethodField()
    average_detailed_rating = serializers.ReadOnlyField()
    
    class Meta:
        model = Review
        fields = [
            'id', 'title', 'content', 'rating', 'quality_rating',
            'timeliness_rating', 'communication_rating', 'value_rating',
            'would_recommend', 'photos', 'reviewer_name', 'provider_name',
            'job_title', 'provider_response', 'response_date',
            'helpful_votes', 'average_detailed_rating', 'created_at'
        ]
    
    def get_reviewer_name(self, obj):
        return f"{obj.reviewer.first_name} {obj.reviewer.last_name}".strip()
    
    def get_helpful_votes(self, obj):
        helpful_count = obj.helpful_votes.filter(is_helpful=True).count()
        total_votes = obj.helpful_votes.count()
        return {
            'helpful': helpful_count,
            'total': total_votes
        }

class ReviewResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewResponse
        fields = ['content']

class ReviewListSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.SerializerMethodField()
    provider_name = serializers.CharField(source='provider.business_name', read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'title', 'rating', 'reviewer_name', 'provider_name',
            'would_recommend', 'created_at'
        ]
    
    def get_reviewer_name(self, obj):
        return f"{obj.reviewer.first_name} {obj.reviewer.last_name}".strip()
