from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Count, Q
from django.utils import timezone

from .models import Notification, NotificationPreference
from .serializers import (
    NotificationSerializer, NotificationListSerializer, 
    NotificationPreferenceSerializer, MarkAsReadSerializer,
    NotificationStatsSerializer
)
from .services import NotificationService

class NotificationListView(ListAPIView):
    """List user's notifications with filtering"""
    serializer_class = NotificationListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Notification.objects.filter(recipient=self.request.user)
        
        # Filter by read status
        is_read = self.request.query_params.get('is_read')
        if is_read is not None:
            queryset = queryset.filter(is_read=is_read.lower() == 'true')
        
        # Filter by type
        notification_type = self.request.query_params.get('type')
        if notification_type:
            queryset = queryset.filter(type=notification_type)
        
        # Filter by priority
        priority = self.request.query_params.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
        
        return queryset.select_related('job', 'provider', 'review', 'payment')
    
    @swagger_auto_schema(
        operation_summary='Get notifications',
        operation_description='Get list of notifications for the authenticated user',
        manual_parameters=[
            openapi.Parameter('is_read', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('type', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('priority', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        ],
        tags=['Notifications']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class NotificationDetailView(RetrieveAPIView):
    """Get notification details"""
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        """Mark notification as read when viewed"""
        notification = self.get_object()
        notification.mark_as_read()
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Get notification details',
        operation_description='Get detailed view of a notification (marks as read)',
        tags=['Notifications']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class MarkNotificationsAsReadView(GenericAPIView):
    """Mark notifications as read"""
    serializer_class = MarkAsReadSerializer
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary='Mark notifications as read',
        operation_description='Mark specific notifications or all notifications as read',
        request_body=MarkAsReadSerializer,
        responses={
            200: openapi.Response(description='Notifications marked as read'),
            400: openapi.Response(description='Invalid request'),
        },
        tags=['Notifications']
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        notification_ids = serializer.validated_data.get('notification_ids', [])
        
        if notification_ids:
            # Mark specific notifications as read
            updated_count = Notification.objects.filter(
                id__in=notification_ids,
                recipient=request.user,
                is_read=False
            ).update(
                is_read=True,
                read_at=timezone.now()
            )
        else:
            # Mark all notifications as read
            updated_count = NotificationService.mark_all_as_read(request.user)
        
        return Response({
            'message': f'{updated_count} notifications marked as read',
            'updated_count': updated_count
        })

class NotificationStatsView(GenericAPIView):
    """Get notification statistics"""
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationStatsSerializer
    
    @swagger_auto_schema(
        operation_summary='Get notification statistics',
        operation_description='Get notification counts and statistics',
        responses={200: NotificationStatsSerializer},
        tags=['Notifications']
    )
    def get(self, request):
        user_notifications = Notification.objects.filter(recipient=request.user)
        
        # Basic counts
        total_count = user_notifications.count()
        unread_count = user_notifications.filter(is_read=False).count()
        
        # Count by type
        by_type = dict(
            user_notifications.values('type')
            .annotate(count=Count('id'))
            .values_list('type', 'count')
        )
        
        # Count by priority
        by_priority = dict(
            user_notifications.values('priority')
            .annotate(count=Count('id'))
            .values_list('priority', 'count')
        )
        
        data = {
            'total_count': total_count,
            'unread_count': unread_count,
            'by_type': by_type,
            'by_priority': by_priority
        }
        
        serializer = self.get_serializer(data)
        return Response(serializer.data)

class NotificationPreferenceView(RetrieveAPIView, UpdateAPIView):
    """Get and update notification preferences"""
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        preferences, created = NotificationPreference.objects.get_or_create(
            user=self.request.user
        )
        return preferences
    
    @swagger_auto_schema(
        operation_summary='Get notification preferences',
        operation_description='Get user notification preferences',
        tags=['Notifications']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Update notification preferences',
        operation_description='Update user notification preferences',
        tags=['Notifications']
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

@swagger_auto_schema(
    method='get',
    operation_summary='Get unread notification count',
    operation_description='Get count of unread notifications for the authenticated user',
    responses={200: openapi.Response(description='Unread count', schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'unread_count': openapi.Schema(type=openapi.TYPE_INTEGER)}
    ))},
    tags=['Notifications']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unread_count_view(request):
    """Get unread notification count"""
    count = NotificationService.get_unread_count(request.user)
    return Response({'unread_count': count})
