from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from decimal import Decimal

User = get_user_model()

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('card', 'Credit/Debit Card'),
        ('paypal', 'PayPal'),
        ('stripe', 'Stripe'),
        ('bank_transfer', 'Bank Transfer'),
        ('mobile_money', 'Mobile Money'),
    ]
    
    # Core relationships
    job = models.OneToOneField('jobs.Job', on_delete=models.CASCADE, related_name='payment')
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments_made')
    provider = models.ForeignKey('providers.Provider', on_delete=models.CASCADE, related_name='payments_received')
    
    # Payment details
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    platform_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    provider_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Payment processing
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # External payment references
    transaction_id = models.CharField(max_length=255, unique=True)
    payment_gateway_id = models.CharField(max_length=255, blank=True)
    payment_gateway_response = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Additional info
    description = models.TextField(blank=True)
    receipt_url = models.URLField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Payment {self.transaction_id} - {self.amount}"
    
    def save(self, *args, **kwargs):
        # Calculate provider amount (total - platform fee)
        if not self.provider_amount:
            self.provider_amount = self.amount - self.platform_fee
        super().save(*args, **kwargs)

class PaymentMethod(models.Model):
    """Stored payment methods for users"""
    CARD_TYPES = [
        ('visa', 'Visa'),
        ('mastercard', 'Mastercard'),
        ('amex', 'American Express'),
        ('discover', 'Discover'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_methods')
    method_type = models.CharField(max_length=20, choices=Payment.PAYMENT_METHOD_CHOICES)
    
    # Card details (encrypted/tokenized)
    card_last_four = models.CharField(max_length=4, blank=True)
    card_type = models.CharField(max_length=20, choices=CARD_TYPES, blank=True)
    card_exp_month = models.PositiveIntegerField(null=True, blank=True)
    card_exp_year = models.PositiveIntegerField(null=True, blank=True)
    
    # Payment gateway token
    gateway_token = models.CharField(max_length=255)
    
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.card_last_four:
            return f"{self.get_card_type_display()} ending in {self.card_last_four}"
        return f"{self.get_method_type_display()}"

class PaymentDispute(models.Model):
    DISPUTE_STATUS_CHOICES = [
        ('open', 'Open'),
        ('under_review', 'Under Review'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    DISPUTE_REASON_CHOICES = [
        ('not_delivered', 'Service Not Delivered'),
        ('poor_quality', 'Poor Quality Work'),
        ('overcharged', 'Overcharged'),
        ('unauthorized', 'Unauthorized Payment'),
        ('damaged_property', 'Damaged Property'),
        ('other', 'Other'),
    ]
    
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='dispute')
    disputed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_disputes')
    
    reason = models.CharField(max_length=20, choices=DISPUTE_REASON_CHOICES)
    description = models.TextField()
    evidence_files = models.JSONField(default=list, blank=True)
    
    status = models.CharField(max_length=20, choices=DISPUTE_STATUS_CHOICES, default='open')
    admin_notes = models.TextField(blank=True)
    resolution_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Dispute for Payment {self.payment.transaction_id}"

class Refund(models.Model):
    REFUND_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='refunds')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    reason = models.TextField()
    
    status = models.CharField(max_length=20, choices=REFUND_STATUS_CHOICES, default='pending')
    gateway_refund_id = models.CharField(max_length=255, blank=True)
    
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='processed_refunds')
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Refund {self.amount} for Payment {self.payment.transaction_id}"

class PayoutRequest(models.Model):
    """Provider payout requests"""
    PAYOUT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]
    
    provider = models.ForeignKey('providers.Provider', on_delete=models.CASCADE, related_name='payout_requests')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    
    # Bank details
    bank_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50)
    account_holder_name = models.CharField(max_length=255)
    routing_number = models.CharField(max_length=20, blank=True)
    
    status = models.CharField(max_length=20, choices=PAYOUT_STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='processed_payouts')
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Payout Request {self.amount} for {self.provider.business_name}"
