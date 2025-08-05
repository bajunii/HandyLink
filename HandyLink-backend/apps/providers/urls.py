from django.urls import path
from .views import (
    ProviderRegistrationView,
    ProviderListView,
    ProviderDetailView,
    MyProviderProfileView,
    ProviderServicesView
)

urlpatterns = [
    path('register/', ProviderRegistrationView.as_view(), name='provider-register'),
    path('', ProviderListView.as_view(), name='provider-list'),
    path('<int:id>/', ProviderDetailView.as_view(), name='provider-detail'),
    path('my-profile/', MyProviderProfileView.as_view(), name='my-provider-profile'),
    path('<int:provider_id>/services/', ProviderServicesView.as_view(), name='provider-services'),
]