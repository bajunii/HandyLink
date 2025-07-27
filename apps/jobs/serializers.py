from rest_framework import serializers
from .models import JobCategory, Job, JobApplication, JobReview, JobMessage
from apps.providers.models import Provider

class JobCategorySerializer(serializers.ModelSerializer):
    job_count = serializers.SerializerMethodField()
    
    class Meta:
        model = JobCategory
        fields = ['id', 'name', 'description', 'icon', 'is_active', 'job_count', 'created_at']
        read_only_fields = ['created_at']
    
    def get_job_count(self, obj):
        return obj.jobs.filter(status='open').count()

class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            'title', 'description', 'category', 'budget_min', 'budget_max',
            'location', 'urgency', 'is_remote', 'skills_required', 
            'attachments', 'deadline'
        ]
    
    def validate(self, data):
        if data['budget_min'] > data['budget_max']:
            raise serializers.ValidationError("Minimum budget cannot be greater than maximum budget.")
        return data

class JobSerializer(serializers.ModelSerializer):
    posted_by_name = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)
    assigned_provider_name = serializers.CharField(source='assigned_to.business_name', read_only=True)
    application_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'category', 'category_name',
            'posted_by', 'posted_by_name', 'assigned_to', 'assigned_provider_name',
            'budget_min', 'budget_max', 'location', 'urgency', 'status',
            'is_remote', 'skills_required', 'attachments', 'deadline',
            'application_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['posted_by', 'created_at', 'updated_at']
    
    def get_posted_by_name(self, obj):
        return f"{obj.posted_by.first_name} {obj.posted_by.last_name}".strip()
    
    def get_application_count(self, obj):
        return obj.applications.count()

class JobListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    posted_by_name = serializers.SerializerMethodField()
    application_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'category_name', 'posted_by_name', 'budget_min',
            'budget_max', 'location', 'urgency', 'status', 'is_remote',
            'application_count', 'created_at'
        ]
    
    def get_posted_by_name(self, obj):
        return f"{obj.posted_by.first_name} {obj.posted_by.last_name}".strip()
    
    def get_application_count(self, obj):
        return obj.applications.count()

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
        read_only_fields = ['applied_at', 'updated_at']

class ApplyToJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['bid_amount', 'estimated_duration', 'cover_letter']
    
    def validate_bid_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Bid amount must be greater than 0")
        return value

class JobReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.SerializerMethodField()
    
    class Meta:
        model = JobReview
        fields = ['id', 'rating', 'comment', 'reviewer_name', 'created_at']
        read_only_fields = ['created_at']
    
    def get_reviewer_name(self, obj):
        return f"{obj.reviewer.first_name} {obj.reviewer.last_name}".strip()

class JobMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    
    class Meta:
        model = JobMessage
        fields = ['id', 'sender', 'sender_name', 'message', 'is_read', 'created_at']
        read_only_fields = ['sender', 'created_at']
    
    def get_sender_name(self, obj):
        return f"{obj.sender.first_name} {obj.sender.last_name}".strip()
