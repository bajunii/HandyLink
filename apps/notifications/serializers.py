from rest_framework import serializers
from .models import Notification, NotificationPreference, NotificationTemplate

class NotificationSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    time_ago = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = [
            'id', 'type', 'type_display', 'title', 'message', 'priority', 
            'priority_display', 'is_read', 'action_url', 'data',
            'created_at', 'read_at', 'time_ago'
        ]
        read_only_fields = ['created_at', 'read_at']
    
    def get_time_ago(self, obj):
        """Return human-readable time ago"""
        from django.utils.timesince import timesince
        return timesince(obj.created_at)

class NotificationListSerializer(serializers.ModelSerializer):
    """Simplified serializer for notification lists"""
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'type', 'type_display', 'title', 'priority', 
            'is_read', 'created_at'
        ]

class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = [
            'email_enabled', 'push_enabled', 'job_notifications',
            'payment_notifications', 'review_notifications', 
            'provider_notifications', 'marketing_notifications',
            'instant_notifications', 'daily_digest', 'weekly_summary',
            'quiet_hours_enabled', 'quiet_start', 'quiet_end'
        ]
    
    def validate(self, data):
        """Validate quiet hours"""
        if data.get('quiet_hours_enabled'):
            if not data.get('quiet_start') or not data.get('quiet_end'):
                raise serializers.ValidationError(
                    "Both quiet_start and quiet_end are required when quiet hours are enabled"
                )
        return data

class MarkAsReadSerializer(serializers.Serializer):
    """Serializer for marking notifications as read"""
    notification_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        help_text="List of notification IDs to mark as read. If empty, marks all as read."
    )

class NotificationStatsSerializer(serializers.Serializer):
    """Serializer for notification statistics"""
    total_count = serializers.IntegerField()
    unread_count = serializers.IntegerField()
    by_type = serializers.DictField()
    by_priority = serializers.DictField()
