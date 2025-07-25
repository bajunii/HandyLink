from django.db import models
from django.contrib.auth import get_user_model
from apps.providers.models import Provider

User = get_user_model()

class JobCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Icon class name")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Job Categories"
    
    def __str__(self):
        return self.name

class Job(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('disputed', 'Disputed'),
    ]
    
    URGENCY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    # Relationships
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs')
    assigned_to = models.ForeignKey(Provider, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_jobs')
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE, related_name='jobs')
    
    # Job Details
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    budget_min = models.DecimalField(max_digits=10, decimal_places=2)
    budget_max = models.DecimalField(max_digits=10, decimal_places=2)
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Dates
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Additional Info
    requirements = models.TextField(blank=True, help_text="Special requirements or skills needed")
    is_remote = models.BooleanField(default=False)
    images = models.JSONField(default=list, blank=True, help_text="List of image URLs")
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.posted_by.email}"
    
    @property
    def application_count(self):
        return self.applications.count()
    
    @property
    def budget_range(self):
        return f"${self.budget_min} - ${self.budget_max}"

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    # Relationships
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='job_applications')
    
    # Application Details
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_duration = models.PositiveIntegerField(help_text="Estimated duration in hours")
    cover_letter = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Dates
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['job', 'provider']
        ordering = ['-applied_at']
    
    def __str__(self):
        return f"{self.provider.business_name} applied for {self.job.title}"

class JobReview(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    # Relationships
    job = models.OneToOneField(Job, on_delete=models.CASCADE, related_name='review')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews')
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='received_reviews')
    
    # Review Details
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    would_recommend = models.BooleanField(default=True)
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Review for {self.job.title} - {self.rating} stars"

class JobMessage(models.Model):
    # Relationships
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    
    # Message Details
    message = models.TextField()
    attachment = models.FileField(upload_to='job_messages/', blank=True, null=True)
    is_read = models.BooleanField(default=False)
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Message in {self.job.title} by {self.sender.email}"
