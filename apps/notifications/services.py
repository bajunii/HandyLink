from django.core.mail import send_mail, EmailMessage
from django.template import Template, Context
from django.template.loader import render_to_string, get_template
from django.conf import settings
from django.utils import timezone
from .models import Notification, NotificationTemplate, NotificationPreference
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    """Service to handle notification creation and delivery"""
    
    @staticmethod
    def create_notification(
        recipient,
        notification_type,
        context_data=None,
        related_job=None,
        related_provider=None,
        related_review=None,
        related_payment=None,
        priority='medium',
        action_url=''
    ):
        """
        Create and optionally send a notification
        
        Args:
            recipient: User object
            notification_type: str from NOTIFICATION_TYPES
            context_data: dict with data for template rendering
            related_*: Related model instances
            priority: notification priority
            action_url: URL to navigate when clicked
        """
        context_data = context_data or {}
        
        try:
            # Get or create notification template
            template = NotificationTemplate.objects.filter(
                type=notification_type,
                is_active=True
            ).first()
            
            if not template:
                # Create default template if none exists
                template = NotificationService._create_default_template(notification_type)
            
            # Render title and message
            title = NotificationService._render_template(template.title_template, context_data)
            message = NotificationService._render_template(template.message_template, context_data)
            
            # Create notification
            notification = Notification.objects.create(
                recipient=recipient,
                type=notification_type,
                title=title,
                message=message,
                priority=priority,
                job=related_job,
                provider=related_provider,
                review=related_review,
                payment=related_payment,
                data=context_data,
                action_url=action_url
            )
            
            # Send notification if user preferences allow
            NotificationService._send_notification(notification, template)
            
            return notification
            
        except Exception as e:
            logger.error(f"Error creating notification: {e}")
            return None
    
    @staticmethod
    def _render_template(template_string, context_data):
        """Render template string with context data"""
        try:
            template = Template(template_string)
            context = Context(context_data)
            return template.render(context)
        except Exception as e:
            logger.error(f"Error rendering template: {e}")
            return template_string
    
    @staticmethod
    def _send_notification(notification, template):
        """Send notification via enabled channels"""
        try:
            # Get user preferences
            preferences = NotificationService._get_user_preferences(notification.recipient)
            
            # Check if notification type is enabled
            if not NotificationService._is_notification_type_enabled(notification.type, preferences):
                return
            
            # Send email if enabled
            if preferences.email_enabled and template.send_email:
                NotificationService._send_email(notification, template, preferences)
            
            # Mark as sent
            notification.mark_as_sent()
            
        except Exception as e:
            logger.error(f"Error sending notification: {e}")
    
    @staticmethod
    def _send_email(notification, template, preferences):
        """Send email notification with HTML styling"""
        try:
            # Skip if user disabled email notifications
            if not preferences.email_enabled:
                return
            
            # Check quiet hours
            if NotificationService._is_quiet_hours(preferences):
                return
            
            # Prepare context data for template rendering
            context_data = notification.data.copy() if notification.data else {}
            context_data.update({
                'recipient_name': notification.recipient.get_full_name or notification.recipient.email,
                'notification_title': notification.title,
                'notification_message': notification.message,
                'action_url': notification.action_url,
                'priority': notification.priority,
                'notification_type': notification.type,
            })
            
            # Render email subject
            subject = NotificationService._render_template(
                template.email_subject_template or notification.title,
                context_data
            )
            
            # Try to use HTML template first, fallback to text
            html_content = None
            template_name = f"emails/{notification.type}.html"
            
            try:
                # Render HTML email template
                html_content = render_to_string(template_name, context_data)
            except Exception as template_error:
                logger.warning(f"HTML template {template_name} not found: {template_error}")
                # Fallback to generic template
                try:
                    html_content = render_to_string("emails/generic.html", context_data)
                except Exception as generic_error:
                    logger.warning(f"Generic template not found: {generic_error}")
                    # Final fallback to base template
                    try:
                        html_content = render_to_string("emails/base.html", context_data)
                    except Exception as base_error:
                        logger.error(f"Base template not found: {base_error}")
                        html_content = None
            
            # Create email message
            if html_content:
                # Send HTML email
                email = EmailMessage(
                    subject=subject,
                    body=html_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[notification.recipient.email]
                )
                email.content_subtype = "html"  # Set content type to HTML
                
                try:
                    email.send(fail_silently=False)
                    print(f"✅ HTML email sent to {notification.recipient.email}: {subject}")
                except Exception as smtp_error:
                    print(f"❌ SMTP Error: {smtp_error}")
                    logger.error(f"SMTP Error sending email to {notification.recipient.email}: {smtp_error}")
                    raise smtp_error
            else:
                # Fallback to plain text email
                body = NotificationService._render_template(
                    template.email_body_template or notification.message,
                    context_data
                )
                try:
                    send_mail(
                        subject=subject,
                        message=body,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[notification.recipient.email],
                        fail_silently=False,
                    )
                    print(f"✅ Plain text email sent to {notification.recipient.email}: {subject}")
                except Exception as smtp_error:
                    print(f"❌ SMTP Error: {smtp_error}")
                    logger.error(f"SMTP Error sending plain text email to {notification.recipient.email}: {smtp_error}")
                    raise smtp_error
            
            notification.sent_via_email = True
            notification.save(update_fields=['sent_via_email'])
            
        except Exception as e:
            logger.error(f"Error sending email notification: {e}")
    
    @staticmethod
    def _get_user_preferences(user):
        """Get or create user notification preferences"""
        preferences, created = NotificationPreference.objects.get_or_create(
            user=user,
            defaults={
                'email_enabled': True,
                'push_enabled': True,
                'job_notifications': True,
                'payment_notifications': True,
                'review_notifications': True,
                'provider_notifications': True,
            }
        )
        return preferences
    
    @staticmethod
    def _is_notification_type_enabled(notification_type, preferences):
        """Check if notification type is enabled in user preferences"""
        type_mapping = {
            'job_posted': preferences.job_notifications,
            'job_application': preferences.job_notifications,
            'job_assigned': preferences.job_notifications,
            'job_completed': preferences.job_notifications,
            'job_cancelled': preferences.job_notifications,
            'job_deadline': preferences.job_notifications,
            'payment_received': preferences.payment_notifications,
            'payment_failed': preferences.payment_notifications,
            'refund_issued': preferences.payment_notifications,
            'payment_reminder': preferences.payment_notifications,
            'review_received': preferences.review_notifications,
            'review_response': preferences.review_notifications,
            'review_reminder': preferences.review_notifications,
            'provider_approved': preferences.provider_notifications,
            'provider_rejected': preferences.provider_notifications,
            'new_job_match': preferences.provider_notifications,
            'application_response': preferences.provider_notifications,
        }
        return type_mapping.get(notification_type, True)
    
    @staticmethod
    def _is_quiet_hours(preferences):
        """Check if current time is within user's quiet hours"""
        if not preferences.quiet_hours_enabled:
            return False
        
        current_time = timezone.now().time()
        start_time = preferences.quiet_start
        end_time = preferences.quiet_end
        
        if start_time < end_time:
            # Normal case: 22:00 - 08:00 next day
            return start_time <= current_time <= end_time
        else:
            # Overnight case: 22:00 - 08:00 next day
            return current_time >= start_time or current_time <= end_time
    
    @staticmethod
    def _create_default_template(notification_type):
        """Create default template for notification type"""
        templates = {
            'user_welcome': {
                'title': 'Welcome to HandyLink!',
                'message': 'Welcome {user_name}! Your account has been created successfully.',
                'email_subject': 'Welcome to HandyLink - Get Started Today!',
                'email_body': 'Hi {user_name},\n\nWelcome to HandyLink! We\'re excited to have you on board.\n\nBest regards,\nThe HandyLink Team'
            },
            'job_application': {
                'title': 'New Job Application',
                'message': 'You received a new application for "{job_title}" from {provider_name}.',
                'email_subject': 'New Application for Your Job: {job_title}',
                'email_body': 'Hi {user_name},\n\nYou have received a new application for your job "{job_title}" from {provider_name}.\n\nView the application: {action_url}\n\nBest regards,\nThe HandyLink Team'
            },
            'application_response': {
                'title': 'Application Response',
                'message': 'Your application for "{job_title}" has been {status}.',
                'email_subject': 'Application Update for {job_title}',
                'email_body': 'Hi {user_name},\n\nYour application for "{job_title}" has been {status}.\n\nView details: {action_url}\n\nBest regards,\nThe HandyLink Team'
            },
            'payment_received': {
                'title': 'Payment Received',
                'message': 'You have received a payment of ${amount} for "{job_title}".',
                'email_subject': 'Payment Received - ${amount}',
                'email_body': 'Hi {user_name},\n\nYou have received a payment of ${amount} for the job "{job_title}".\n\nView details: {action_url}\n\nBest regards,\nThe HandyLink Team'
            },
            'review_received': {
                'title': 'New Review',
                'message': 'You received a new {rating}-star review for "{job_title}".',
                'email_subject': 'New Review Received',
                'email_body': 'Hi {user_name},\n\nYou have received a new {rating}-star review for your work on "{job_title}".\n\nView review: {action_url}\n\nBest regards,\nThe HandyLink Team'
            }
        }
        
        template_data = templates.get(notification_type, {
            'title': 'HandyLink Notification',
            'message': 'You have a new notification.',
            'email_subject': 'HandyLink Notification',
            'email_body': 'You have a new notification from HandyLink.'
        })
        
        return NotificationTemplate.objects.create(
            type=notification_type,
            title_template=template_data['title'],
            message_template=template_data['message'],
            email_subject_template=template_data['email_subject'],
            email_body_template=template_data['email_body']
        )
    
    @staticmethod
    def mark_all_as_read(user):
        """Mark all notifications as read for a user"""
        return Notification.objects.filter(
            recipient=user,
            is_read=False
        ).update(
            is_read=True,
            read_at=timezone.now()
        )
    
    @staticmethod
    def get_unread_count(user):
        """Get count of unread notifications for a user"""
        return Notification.objects.filter(
            recipient=user,
            is_read=False
        ).count()
