from django.contrib import admin
from .models import Notification, NotificationPreference, NotificationTemplate

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'recipient', 'type', 'priority', 'is_read', 
        'is_sent', 'sent_via_email', 'created_at'
    ]
    list_filter = [
        'type', 'priority', 'is_read', 'is_sent', 'sent_via_email', 'created_at'
    ]
    search_fields = [
        'title', 'message', 'recipient__email', 'recipient__first_name', 
        'recipient__last_name'
    ]
    readonly_fields = ['created_at', 'read_at', 'sent_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('recipient', 'type', 'title', 'message', 'priority')
        }),
        ('Related Objects', {
            'fields': ('job', 'provider', 'review', 'payment'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_read', 'is_sent', 'sent_via_email', 'sent_via_push')
        }),
        ('Additional Data', {
            'fields': ('data', 'action_url'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'read_at', 'sent_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['mark_as_read', 'mark_as_sent']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f"{queryset.count()} notifications marked as read.")
    mark_as_read.short_description = "Mark selected notifications as read"
    
    def mark_as_sent(self, request, queryset):
        queryset.update(is_sent=True)
        self.message_user(request, f"{queryset.count()} notifications marked as sent.")
    mark_as_sent.short_description = "Mark selected notifications as sent"

@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'email_enabled', 'push_enabled', 'job_notifications',
        'payment_notifications', 'review_notifications', 'created_at'
    ]
    list_filter = [
        'email_enabled', 'push_enabled', 'job_notifications',
        'payment_notifications', 'review_notifications', 'created_at'
    ]
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Channel Preferences', {
            'fields': ('email_enabled', 'push_enabled')
        }),
        ('Type Preferences', {
            'fields': (
                'job_notifications', 'payment_notifications', 
                'review_notifications', 'provider_notifications',
                'marketing_notifications'
            )
        }),
        ('Frequency Preferences', {
            'fields': ('instant_notifications', 'daily_digest', 'weekly_summary')
        }),
        ('Quiet Hours', {
            'fields': ('quiet_hours_enabled', 'quiet_start', 'quiet_end'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = [
        'type', 'title_template', 'send_email', 'send_push', 
        'is_active', 'created_at'
    ]
    list_filter = ['type', 'send_email', 'send_push', 'is_active', 'created_at']
    search_fields = ['type', 'title_template', 'message_template']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Template Information', {
            'fields': ('type', 'is_active')
        }),
        ('In-App Templates', {
            'fields': ('title_template', 'message_template')
        }),
        ('Email Templates', {
            'fields': ('email_subject_template', 'email_body_template')
        }),
        ('Delivery Settings', {
            'fields': ('send_email', 'send_push')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Add help text for template variables
        help_text = (
            "Available variables: {user_name}, {job_title}, {provider_name}, "
            "{amount}, {rating}, {status}, {action_url}"
        )
        form.base_fields['title_template'].help_text = help_text
        form.base_fields['message_template'].help_text = help_text
        return form
