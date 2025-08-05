from django.db import models
from django.contrib.auth import get_user_model
from apps.providers.models import Provider

User = get_user_model()

class JobCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Icon class or emoji")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Job Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class Job(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    URGENCY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('emergency', 'Emergency'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE, related_name='jobs')
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs')
    assigned_to = models.ForeignKey(Provider, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_jobs')
    
    budget_min = models.DecimalField(max_digits=10, decimal_places=2)
    budget_max = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    
    is_remote = models.BooleanField(default=False)
    skills_required = models.JSONField(default=list, blank=True)
    attachments = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.posted_by.email}"

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='job_applications')
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_duration = models.CharField(max_length=100)
    cover_letter = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['job', 'provider']
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.provider.business_name} applied to {self.job.title}"

class JobReview(models.Model):
    job = models.OneToOneField(Job, on_delete=models.CASCADE, related_name='job_review')  # Changed related_name
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_reviews_written')
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='job_reviews_received')
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.job.title} - {self.rating} stars"

class JobMessage(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_job_messages')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message in {self.job.title} from {self.sender.email}"
