from django.urls import path
from .views import (
    NotificationListView,
    NotificationDetailView,
    MarkNotificationsAsReadView,
    NotificationStatsView,
    NotificationPreferenceView,
    unread_count_view
)

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
    path('mark-read/', MarkNotificationsAsReadView.as_view(), name='mark-notifications-read'),
    path('stats/', NotificationStatsView.as_view(), name='notification-stats'),
    path('preferences/', NotificationPreferenceView.as_view(), name='notification-preferences'),
    path('unread-count/', unread_count_view, name='unread-count'),
]
