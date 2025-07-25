from rest_framework import serializers
from .models import Job, JobCategory, JobApplication, JobReview, JobMessage
from apps.users.serializers import UserSerializer
from apps.providers.serializers import ProviderSerializer

class JobCategorySerializer(serializers.ModelSerializer):
    job_count = serializers.SerializerMethodField()
    
    class Meta:
        model = JobCategory
        fields = ['id', 'name', 'description', 'icon', 'is_active', 'job_count', 'created_at']
        read_only_fields = ['created_at']
    
    def get_job_count(self, obj):
        return obj.jobs.filter(status='open').count()

class JobApplicationSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(source='provider.business_name', read_only=True)
    provider_rating = serializers.DecimalField(source='provider.rating', max_digits=3, decimal_places=2, read_only=True)
    
    class Meta:
        model = JobApplication
        fields = [
            'id', 'job', 'provider', 'provider_name', 'provider_rating',
            'bid_amount', 'estimated_duration', 'cover_letter', 'status',
            'applied_at', 'updated_at'
        ]
        read_only_fields = ['applied_at', 'updated_at', 'status']

class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            'title', 'description', 'category', 'location', 'budget_min', 'budget_max',
            'urgency', 'start_date', 'end_date', 'deadline', 'requirements',
            'is_remote', 'images'
        ]
    
    def validate(self, data):
        if data['budget_min'] > data['budget_max']:
            raise serializers.ValidationError("Minimum budget cannot be greater than maximum budget.")
        
        if data.get('start_date') and data.get('end_date'):
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError("Start date cannot be after end date.")
        
        return data
    
    def create(self, validated_data):
        validated_data['posted_by'] = self.context['request'].user
        return super().create(validated_data)

class JobSerializer(serializers.ModelSerializer):
    posted_by_name = serializers.SerializerMethodField()
    assigned_to_name = serializers.CharField(source='assigned_to.business_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    application_count = serializers.ReadOnlyField()
    budget_range = serializers.ReadOnlyField()
    applications = JobApplicationSerializer(many=True, read_only=True)
    
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'category', 'category_name', 'location',
            'budget_min', 'budget_max', 'budget_range', 'urgency', 'status',
            'posted_by', 'posted_by_name', 'assigned_to', 'assigned_to_name',
            'start_date', 'end_date', 'deadline', 'requirements', 'is_remote',
            'images', 'application_count', 'applications', 'created_at', 'updated_at'
        ]
        read_only_fields = ['posted_by', 'application_count', 'created_at', 'updated_at']
    
    def get_posted_by_name(self, obj):
        return f"{obj.posted_by.first_name} {obj.posted_by.last_name}".strip()

class JobListSerializer(serializers.ModelSerializer):
    """Simplified serializer for job listings"""
    posted_by_name = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)
    application_count = serializers.ReadOnlyField()
    budget_range = serializers.ReadOnlyField()
    
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'category_name', 'location',
            'budget_range', 'urgency', 'status', 'posted_by_name',
            'application_count', 'deadline', 'is_remote', 'created_at'
        ]
    
    def get_posted_by_name(self, obj):
        return f"{obj.posted_by.first_name} {obj.posted_by.last_name}".strip()

class JobReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.SerializerMethodField()
    
    class Meta:
        model = JobReview
        fields = [
            'id', 'job', 'reviewer', 'reviewer_name', 'provider', 'rating',
            'comment', 'would_recommend', 'created_at', 'updated_at'
        ]
        read_only_fields = ['reviewer', 'created_at', 'updated_at']
    
    def get_reviewer_name(self, obj):
        return f"{obj.reviewer.first_name} {obj.reviewer.last_name}".strip()

class JobMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    
    class Meta:
        model = JobMessage
        fields = [
            'id', 'job', 'sender', 'sender_name', 'message',
            'attachment', 'is_read', 'created_at'
        ]
        read_only_fields = ['sender', 'created_at']
    
    def get_sender_name(self, obj):
        return f"{obj.sender.first_name} {obj.sender.last_name}".strip()

class ApplyToJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['bid_amount', 'estimated_duration', 'cover_letter']
    
    def validate_bid_amount(self, value):
        job = self.context['job']
        if value < job.budget_min or value > job.budget_max:
            raise serializers.ValidationError(
                f"Bid amount must be between ${job.budget_min} and ${job.budget_max}"
            )
        return value
    
    def create(self, validated_data):
        validated_data['job'] = self.context['job']
        validated_data['provider'] = self.context['request'].user.provider_profile
        return super().create(validated_data)
