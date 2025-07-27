from django.urls import path
from .views import (
    CreatePaymentView,
    PaymentHistoryView,
    ProviderEarningsView,
    CreatePaymentDisputeView,
    CreatePayoutRequestView,
    MyPayoutRequestsView
)

urlpatterns = [
    path('jobs/<int:job_id>/pay/', CreatePaymentView.as_view(), name='create-payment'),
    path('my-payments/', PaymentHistoryView.as_view(), name='payment-history'),
    path('my-earnings/', ProviderEarningsView.as_view(), name='provider-earnings'),
    path('payments/<int:payment_id>/dispute/', CreatePaymentDisputeView.as_view(), name='create-dispute'),
    path('payout-requests/', CreatePayoutRequestView.as_view(), name='create-payout-request'),
    path('my-payout-requests/', MyPayoutRequestsView.as_view(), name='my-payout-requests'),
]
