from rest_framework import serializers
from .models import Payment, PaymentMethod, PaymentDispute, Refund, PayoutRequest

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = [
            'id', 'method_type', 'card_last_four', 'card_type',
            'card_exp_month', 'card_exp_year', 'is_default', 'created_at'
        ]
        read_only_fields = ['created_at']

class CreatePaymentSerializer(serializers.ModelSerializer):
    payment_method_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Payment
        fields = ['amount', 'payment_method_id', 'description']
    
    def validate_payment_method_id(self, value):
        if value:
            user = self.context['request'].user
            try:
                payment_method = PaymentMethod.objects.get(id=value, user=user, is_active=True)
                return value
            except PaymentMethod.DoesNotExist:
                raise serializers.ValidationError("Invalid payment method")
        return value

class PaymentSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    provider_name = serializers.CharField(source='provider.business_name', read_only=True)
    payer_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Payment
        fields = [
            'id', 'job_title', 'provider_name', 'payer_name',
            'amount', 'platform_fee', 'provider_amount',
            'payment_method', 'status', 'transaction_id',
            'created_at', 'processed_at', 'completed_at',
            'description', 'receipt_url'
        ]
    
    def get_payer_name(self, obj):
        return f"{obj.payer.first_name} {obj.payer.last_name}"

class PaymentDisputeSerializer(serializers.ModelSerializer):
    payment_info = PaymentSerializer(source='payment', read_only=True)
    
    class Meta:
        model = PaymentDispute
        fields = [
            'id', 'payment_info', 'reason', 'description',
            'evidence_files', 'status', 'admin_notes',
            'resolution_notes', 'created_at', 'resolved_at'
        ]
        read_only_fields = ['admin_notes', 'resolution_notes', 'resolved_at']

class CreatePaymentDisputeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDispute
        fields = ['reason', 'description', 'evidence_files']

class RefundSerializer(serializers.ModelSerializer):
    payment_info = PaymentSerializer(source='payment', read_only=True)
    
    class Meta:
        model = Refund
        fields = [
            'id', 'payment_info', 'amount', 'reason', 'status',
            'created_at', 'processed_at'
        ]

class PayoutRequestSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(source='provider.business_name', read_only=True)
    
    class Meta:
        model = PayoutRequest
        fields = [
            'id', 'provider_name', 'amount', 'bank_name',
            'account_number', 'account_holder_name', 'routing_number',
            'status', 'admin_notes', 'created_at', 'processed_at'
        ]
        read_only_fields = ['admin_notes', 'processed_at']

class CreatePayoutRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayoutRequest
        fields = [
            'amount', 'bank_name', 'account_number',
            'account_holder_name', 'routing_number'
        ]
