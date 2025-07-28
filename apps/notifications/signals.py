from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from apps.jobs.models import Job, JobApplication
from apps.reviews.models import Review
from apps.payments.models import Payment
from apps.providers.models import Provider
from .services import NotificationService

User = get_user_model()

# User-related signals
@receiver(post_save, sender=User)
def user_created_notification(sender, instance, created, **kwargs):
    """Send welcome notification when user is created and verified"""
    if created and instance.is_verified:
        # Only send welcome notification if user is already verified
        print(f"🔥 Signal triggered for verified user: {instance.email}")
        
        try:
            notification = NotificationService.create_notification(
                recipient=instance,
                notification_type='user_welcome',
                context_data={
                    'user_name': instance.get_full_name or instance.email,
                },
                priority='medium'
            )
            print(f"✅ Welcome notification created: {notification.title if notification else 'Failed'}")
        except Exception as e:
            print(f"❌ Error creating notification: {e}")
            import traceback
            traceback.print_exc()
    elif created:
        print(f"👤 User registered but not verified yet: {instance.email} - No welcome email sent")

@receiver(post_save, sender=User)
def user_verified_notification(sender, instance, created, **kwargs):
    """Send welcome notification when user becomes verified"""
    if not created and instance.is_verified:
        # Check if user was just verified (not already verified)
        if not getattr(instance, '_was_verified', False):
            print(f"✅ User verified: {instance.email} - Sending welcome notification")
            
            try:
                notification = NotificationService.create_notification(
                    recipient=instance,
                    notification_type='user_welcome',
                    context_data={
                        'user_name': instance.get_full_name or instance.email,
                    },
                    priority='medium'
                )
                print(f"✅ Welcome notification sent after verification: {notification.title if notification else 'Failed'}")
            except Exception as e:
                print(f"❌ Error creating welcome notification: {e}")
                import traceback
                traceback.print_exc()

# Provider-related signals
@receiver(post_save, sender=Provider)
def provider_status_notification(sender, instance, created, **kwargs):
    """Send notification when provider status changes"""
    if not created and instance.status != getattr(instance, '_original_status', None):
        if instance.status == 'approved':
            NotificationService.create_notification(
                recipient=instance.user,
                notification_type='provider_approved',
                context_data={
                    'user_name': instance.user.get_full_name or instance.user.email,
                    'business_name': instance.business_name,
                },
                related_provider=instance,
                priority='high'
            )
        elif instance.status == 'rejected':
            NotificationService.create_notification(
                recipient=instance.user,
                notification_type='provider_rejected',
                context_data={
                    'user_name': instance.user.get_full_name or instance.user.email,
                    'business_name': instance.business_name,
                },
                related_provider=instance,
                priority='high'
            )

# Job-related signals
@receiver(post_save, sender=JobApplication)
def job_application_notification(sender, instance, created, **kwargs):
    """Send notification when someone applies to a job"""
    if created:
        # Notify job poster about new application
        NotificationService.create_notification(
            recipient=instance.job.posted_by,
            notification_type='job_application',
            context_data={
                'user_name': instance.job.posted_by.get_full_name or instance.job.posted_by.email,
                'job_title': instance.job.title,
                'provider_name': instance.provider.business_name,
                'bid_amount': str(instance.bid_amount),
            },
            related_job=instance.job,
            related_provider=instance.provider,
            priority='medium',
            action_url=f'/jobs/{instance.job.id}/applications/'
        )

@receiver(post_save, sender=JobApplication)
def application_status_notification(sender, instance, created, **kwargs):
    """Send notification when application status changes"""
    if not created:
        old_status = getattr(instance, '_original_status', None)
        if instance.status != old_status and instance.status in ['accepted', 'rejected']:
            NotificationService.create_notification(
                recipient=instance.provider.user,
                notification_type='application_response',
                context_data={
                    'user_name': instance.provider.user.get_full_name or instance.provider.user.email,
                    'job_title': instance.job.title,
                    'status': instance.status,
                },
                related_job=instance.job,
                priority='high',
                action_url=f'/jobs/{instance.job.id}/'
            )

@receiver(post_save, sender=Job)
def job_status_notification(sender, instance, created, **kwargs):
    """Send notification when job status changes"""
    if not created:
        old_status = getattr(instance, '_original_status', None)
        if instance.status != old_status:
            if instance.status == 'completed' and instance.assigned_to:
                # Notify both job poster and provider
                # Notify job poster to review
                NotificationService.create_notification(
                    recipient=instance.posted_by,
                    notification_type='job_completed',
                    context_data={
                        'user_name': instance.posted_by.get_full_name or instance.posted_by.email,
                        'job_title': instance.title,
                        'provider_name': instance.assigned_to.business_name,
                    },
                    related_job=instance,
                    priority='medium',
                    action_url=f'/jobs/{instance.id}/review/'
                )
                
                # Notify provider
                NotificationService.create_notification(
                    recipient=instance.assigned_to.user,
                    notification_type='job_completed',
                    context_data={
                        'user_name': instance.assigned_to.user.get_full_name or instance.assigned_to.user.email,
                        'job_title': instance.title,
                    },
                    related_job=instance,
                    priority='medium',
                    action_url=f'/jobs/{instance.id}/'
                )
            
            elif instance.status == 'cancelled':
                # Notify assigned provider if job is cancelled
                if instance.assigned_to:
                    NotificationService.create_notification(
                        recipient=instance.assigned_to.user,
                        notification_type='job_cancelled',
                        context_data={
                            'user_name': instance.assigned_to.user.get_full_name or instance.assigned_to.user.email,
                            'job_title': instance.title,
                        },
                        related_job=instance,
                        priority='high',
                        action_url=f'/jobs/{instance.id}/'
                    )

# Review-related signals
@receiver(post_save, sender=Review)
def review_notification(sender, instance, created, **kwargs):
    """Send notification when review is created or provider responds"""
    if created:
        # Notify provider about new review
        NotificationService.create_notification(
            recipient=instance.provider.user,
            notification_type='review_received',
            context_data={
                'user_name': instance.provider.user.get_full_name or instance.provider.user.email,
                'job_title': instance.job.title,
                'rating': instance.rating,
                'reviewer_name': instance.reviewer.get_full_name or instance.reviewer.email,
            },
            related_review=instance,
            related_job=instance.job,
            priority='medium',
            action_url=f'/reviews/{instance.id}/'
        )
    else:
        # Check if provider responded to review
        old_response = getattr(instance, '_original_provider_response', None)
        if instance.provider_response and instance.provider_response != old_response:
            NotificationService.create_notification(
                recipient=instance.reviewer,
                notification_type='review_response',
                context_data={
                    'user_name': instance.reviewer.get_full_name or instance.reviewer.email,
                    'job_title': instance.job.title,
                    'provider_name': instance.provider.business_name,
                },
                related_review=instance,
                related_job=instance.job,
                priority='low',
                action_url=f'/reviews/{instance.id}/'
            )

# Payment-related signals
@receiver(post_save, sender=Payment)
def payment_notification(sender, instance, created, **kwargs):
    """Send notification when payment status changes"""
    if not created:
        old_status = getattr(instance, '_original_status', None)
        if instance.status != old_status:
            if instance.status == 'completed':
                # Notify provider about payment received
                NotificationService.create_notification(
                    recipient=instance.provider.user,
                    notification_type='payment_received',
                    context_data={
                        'user_name': instance.provider.user.get_full_name or instance.provider.user.email,
                        'job_title': instance.job.title,
                        'amount': str(instance.provider_amount),
                    },
                    related_payment=instance,
                    related_job=instance.job,
                    priority='high',
                    action_url=f'/payments/{instance.id}/'
                )
                
                # Notify customer about successful payment
                NotificationService.create_notification(
                    recipient=instance.payer,
                    notification_type='payment_received',
                    context_data={
                        'user_name': instance.payer.get_full_name or instance.payer.email,
                        'job_title': instance.job.title,
                        'amount': str(instance.amount),
                        'provider_name': instance.provider.business_name,
                    },
                    related_payment=instance,
                    related_job=instance.job,
                    priority='medium',
                    action_url=f'/payments/{instance.id}/'
                )
            
            elif instance.status == 'failed':
                # Notify customer about failed payment
                NotificationService.create_notification(
                    recipient=instance.payer,
                    notification_type='payment_failed',
                    context_data={
                        'user_name': instance.payer.get_full_name or instance.payer.email,
                        'job_title': instance.job.title,
                        'amount': str(instance.amount),
                    },
                    related_payment=instance,
                    related_job=instance.job,
                    priority='urgent',
                    action_url=f'/payments/{instance.id}/'
                )

# Signal to track original values for comparison
@receiver(post_save, sender=Provider)
def save_original_provider_values(sender, instance, **kwargs):
    """Save original values to track changes"""
    if instance.pk:
        try:
            original = Provider.objects.get(pk=instance.pk)
            instance._original_status = original.status
        except Provider.DoesNotExist:
            pass

@receiver(post_save, sender=JobApplication)
def save_original_application_values(sender, instance, **kwargs):
    """Save original values to track changes"""
    if instance.pk:
        try:
            original = JobApplication.objects.get(pk=instance.pk)
            instance._original_status = original.status
        except JobApplication.DoesNotExist:
            pass

@receiver(post_save, sender=Job)
def save_original_job_values(sender, instance, **kwargs):
    """Save original values to track changes"""
    if instance.pk:
        try:
            original = Job.objects.get(pk=instance.pk)
            instance._original_status = original.status
        except Job.DoesNotExist:
            pass

@receiver(post_save, sender=Review)
def save_original_review_values(sender, instance, **kwargs):
    """Save original values to track changes"""
    if instance.pk:
        try:
            original = Review.objects.get(pk=instance.pk)
            instance._original_provider_response = original.provider_response
        except Review.DoesNotExist:
            pass

@receiver(post_save, sender=User)
def save_original_user_values(sender, instance, **kwargs):
    """Save original values to track changes"""
    if instance.pk:
        try:
            original = User.objects.get(pk=instance.pk)
            instance._was_verified = original.is_verified
        except User.DoesNotExist:
            instance._was_verified = False

@receiver(post_save, sender=Payment)
def save_original_payment_values(sender, instance, **kwargs):
    """Save original values to track changes"""
    if instance.pk:
        try:
            original = Payment.objects.get(pk=instance.pk)
            instance._original_status = original.status
        except Payment.DoesNotExist:
            pass
