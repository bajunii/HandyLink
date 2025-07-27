from django.contrib import admin
from .models import Payment, PaymentMethod, Refund

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'job', 'payer', 'provider', 'amount', 'status', 
        'payment_method', 'created_at'
    ]
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = [
        'job__title', 'payer__email', 'provider__business_name', 
        'transaction_id', 'payment_gateway_id'
    ]
    readonly_fields = ['created_at', 'processed_at', 'completed_at', 'transaction_id']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('job', 'payer', 'provider', 'amount', 'platform_fee', 'provider_amount')
        }),
        ('Payment Details', {
            'fields': ('payment_method', 'status', 'transaction_id', 'payment_gateway_id')
        }),
        ('Additional Information', {
            'fields': ('description', 'receipt_url'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'processed_at', 'completed_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['user', 'method_type', 'card_last_four', 'is_default', 'is_active', 'created_at']
    list_filter = ['method_type', 'is_default', 'is_active', 'created_at']
    search_fields = ['user__email', 'card_last_four', 'gateway_token']
    readonly_fields = ['created_at']

@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ['payment', 'amount', 'status', 'reason', 'created_at']
    list_filter = ['status', 'reason', 'created_at']
    search_fields = ['payment__transaction_id', 'gateway_refund_id']
    readonly_fields = ['created_at']
