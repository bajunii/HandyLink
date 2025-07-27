from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        # User-related
        ('user_welcome', 'Welcome'),
        ('user_verification', 'Email Verification'),
        ('user_security', 'Security Alert'),
        
        # Provider-related
        ('provider_approved', 'Provider Approved'),
        ('provider_rejected', 'Provider Rejected'),
        ('new_job_match', 'New Job Match'),
        ('application_response', 'Application Response'),
        
        # Job-related
        ('job_posted', 'Job Posted'),
        ('job_application', 'New Job Application'),
        ('job_assigned', 'Job Assigned'),
        ('job_completed', 'Job Completed'),
        ('job_cancelled', 'Job Cancelled'),
        ('job_deadline', 'Job Deadline Reminder'),
        
        # Review-related
        ('review_received', 'Review Received'),
        ('review_response', 'Review Response'),
        ('review_reminder', 'Review Reminder'),
        
        # Payment-related
        ('payment_received', 'Payment Received'),
        ('payment_failed', 'Payment Failed'),
        ('refund_issued', 'Refund Issued'),
        ('payment_reminder', 'Payment Reminder'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    # Core fields
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    # Related objects (optional foreign keys)
    job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    provider = models.ForeignKey('providers.Provider', on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    review = models.ForeignKey('reviews.Review', on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    payment = models.ForeignKey('payments.Payment', on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    
    # Delivery status
    is_read = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    sent_via_email = models.BooleanField(default=False)
    sent_via_push = models.BooleanField(default=False)
    
    # Additional data
    data = models.JSONField(default=dict, blank=True, help_text="Additional data for the notification")
    action_url = models.URLField(blank=True, help_text="URL to navigate when notification is clicked")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['type', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.recipient.email}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])
    
    def mark_as_sent(self):
        """Mark notification as sent"""
        if not self.is_sent:
            self.is_sent = True
            self.sent_at = timezone.now()
            self.save(update_fields=['is_sent', 'sent_at'])

class NotificationPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    
    # Channel preferences
    email_enabled = models.BooleanField(default=True)
    push_enabled = models.BooleanField(default=True)
    
    # Type preferences
    job_notifications = models.BooleanField(default=True)
    payment_notifications = models.BooleanField(default=True)
    review_notifications = models.BooleanField(default=True)
    provider_notifications = models.BooleanField(default=True)
    marketing_notifications = models.BooleanField(default=False)
    
    # Frequency preferences
    instant_notifications = models.BooleanField(default=True)
    daily_digest = models.BooleanField(default=True)
    weekly_summary = models.BooleanField(default=False)
    
    # Quiet hours
    quiet_hours_enabled = models.BooleanField(default=False)
    quiet_start = models.TimeField(default='22:00', help_text="Start of quiet hours (24h format)")
    quiet_end = models.TimeField(default='08:00', help_text="End of quiet hours (24h format)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Notification preferences for {self.user.email}"

class NotificationTemplate(models.Model):
    """Template for different notification types"""
    type = models.CharField(max_length=50, choices=Notification.NOTIFICATION_TYPES, unique=True)
    title_template = models.CharField(max_length=255, help_text="Use {variable} for dynamic content")
    message_template = models.TextField(help_text="Use {variable} for dynamic content")
    email_subject_template = models.CharField(max_length=255, blank=True)
    email_body_template = models.TextField(blank=True)
    
    # Delivery settings
    send_email = models.BooleanField(default=True)
    send_push = models.BooleanField(default=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Template for {self.get_type_display()}"
