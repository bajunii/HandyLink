from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils import timezone
import uuid

from .models import Payment, PaymentMethod, PaymentDispute, PayoutRequest
from .serializers import (
    CreatePaymentSerializer, PaymentSerializer, PaymentMethodSerializer,
    CreatePaymentDisputeSerializer, PaymentDisputeSerializer,
    CreatePayoutRequestSerializer, PayoutRequestSerializer
)
from apps.jobs.models import Job

class CreatePaymentView(GenericAPIView):
    serializer_class = CreatePaymentSerializer
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary='Create payment for job',
        operation_description="""
        Process payment for a completed job.
        
        **Requirements:**
        - Job must be completed
        - User must be the job poster
        - Payment hasn't been made yet
        """,
        responses={
            201: openapi.Response(description='Payment processed successfully'),
            400: openapi.Response(description='Payment failed')
        },
        tags=['Payments']
    )
    def post(self, request, job_id):
        try:
            job = Job.objects.get(
                id=job_id,
                posted_by=request.user,
                status='completed'
            )
            
            # Check if payment already exists
            if hasattr(job, 'payment'):
                return Response({
                    'message': 'Payment already exists for this job'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if not job.assigned_to:
                return Response({
                    'message': 'No provider assigned to this job'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                # Calculate platform fee (5% of job amount)
                amount = serializer.validated_data['amount']
                platform_fee = amount * 0.05  # 5% platform fee
                
                # Create payment
                payment = Payment.objects.create(
                    job=job,
                    payer=request.user,
                    provider=job.assigned_to,
                    amount=amount,
                    platform_fee=platform_fee,
                    payment_method='card',  # Default for now
                    transaction_id=str(uuid.uuid4()),
                    description=serializer.validated_data.get('description', ''),
                    status='processing'
                )
                
                # Simulate payment processing
                success = self.process_payment(payment)
                
                if success:
                    payment.status = 'completed'
                    payment.completed_at = timezone.now()
                    payment.save()
                    
                    return Response({
                        'message': 'Payment processed successfully',
                        'payment_id': payment.id,
                        'transaction_id': payment.transaction_id
                    }, status=status.HTTP_201_CREATED)
                else:
                    payment.status = 'failed'
                    payment.save()
                    
                    return Response({
                        'message': 'Payment processing failed'
                    }, status=status.HTTP_400_BAD_REQUEST)
                    
        except Job.DoesNotExist:
            return Response({
                'message': 'Job not found or not eligible for payment'
            }, status=status.HTTP_404_NOT_FOUND)
    
    def process_payment(self, payment):
        """Simulate payment processing - integrate with real payment gateway"""
        # This would integrate with Stripe, PayPal, etc.
        # For now, simulate success
        return True

class PaymentHistoryView(ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Payment.objects.filter(payer=self.request.user).select_related(
            'job', 'provider'
        )
    
    @swagger_auto_schema(
        operation_summary='Get payment history',
        operation_description='Returns payment history for the authenticated user.',
        tags=['Payments']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ProviderEarningsView(ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if not hasattr(self.request.user, 'provider_profile'):
            return Payment.objects.none()
        
        return Payment.objects.filter(
            provider=self.request.user.provider_profile,
            status='completed'
        ).select_related('job', 'payer')
    
    @swagger_auto_schema(
        operation_summary='Get provider earnings',
        operation_description='Returns earnings for the authenticated provider.',
        tags=['Payments']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class CreatePaymentDisputeView(GenericAPIView):
    serializer_class = CreatePaymentDisputeSerializer
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary='Create payment dispute',
        operation_description='Create a dispute for a payment.',
        tags=['Payments']
    )
    def post(self, request, payment_id):
        try:
            payment = Payment.objects.get(
                id=payment_id,
                payer=request.user,
                status='completed'
            )
            
            # Check if dispute already exists
            if hasattr(payment, 'dispute'):
                return Response({
                    'message': 'Dispute already exists for this payment'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                dispute = serializer.save(
                    payment=payment,
                    disputed_by=request.user
                )
                
                return Response({
                    'message': 'Dispute created successfully',
                    'dispute_id': dispute.id
                }, status=status.HTTP_201_CREATED)
                
        except Payment.DoesNotExist:
            return Response({
                'message': 'Payment not found'
            }, status=status.HTTP_404_NOT_FOUND)

class CreatePayoutRequestView(GenericAPIView):
    serializer_class = CreatePayoutRequestSerializer
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary='Request payout',
        operation_description='Create a payout request for provider earnings.',
        tags=['Payments']
    )
    def post(self, request):
        if not hasattr(request.user, 'provider_profile'):
            return Response({
                'message': 'You must be a provider to request payouts'
            }, status=status.HTTP_403_FORBIDDEN)
        
        provider = request.user.provider_profile
        
        # Calculate available balance
        completed_payments = Payment.objects.filter(
            provider=provider,
            status='completed'
        )
        total_earnings = sum(p.provider_amount for p in completed_payments)
        
        # Subtract pending payouts
        pending_payouts = PayoutRequest.objects.filter(
            provider=provider,
            status__in=['pending', 'approved', 'processing']
        )
        pending_amount = sum(p.amount for p in pending_payouts)
        
        available_balance = total_earnings - pending_amount
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            requested_amount = serializer.validated_data['amount']
            
            if requested_amount > available_balance:
                return Response({
                    'message': f'Insufficient balance. Available: ${available_balance}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            payout_request = serializer.save(provider=provider)
            
            return Response({
                'message': 'Payout request created successfully',
                'payout_request_id': payout_request.id
            }, status=status.HTTP_201_CREATED)

class MyPayoutRequestsView(ListAPIView):
    serializer_class = PayoutRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if not hasattr(self.request.user, 'provider_profile'):
            return PayoutRequest.objects.none()
        
        return PayoutRequest.objects.filter(
            provider=self.request.user.provider_profile
        )
    
    @swagger_auto_schema(
        operation_summary='Get my payout requests',
        operation_description='Returns payout requests for the authenticated provider.',
        tags=['Payments']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
