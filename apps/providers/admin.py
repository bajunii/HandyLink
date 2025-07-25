from django.contrib import admin
from .models import Provider, ProviderService, ProviderDocument

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'user', 'provider_type', 'status', 'is_verified', 'rating', 'created_at']
    list_filter = ['provider_type', 'status', 'is_verified', 'created_at']
    search_fields = ['business_name', 'user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['rating', 'total_reviews', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'business_name', 'provider_type', 'description')
        }),
        ('Contact Information', {
            'fields': ('website', 'phone_number', 'address')
        }),
        ('Status & Verification', {
            'fields': ('status', 'is_verified', 'rating', 'total_reviews')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_providers', 'reject_providers', 'verify_providers']
    
    def approve_providers(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, f"{queryset.count()} providers have been approved.")
    approve_providers.short_description = "Approve selected providers"
    
    def reject_providers(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f"{queryset.count()} providers have been rejected.")
    reject_providers.short_description = "Reject selected providers"
    
    def verify_providers(self, request, queryset):
        queryset.update(is_verified=True)
        self.message_user(request, f"{queryset.count()} providers have been verified.")
    verify_providers.short_description = "Verify selected providers"

@admin.register(ProviderService)
class ProviderServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'provider', 'price', 'duration', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at', 'provider__provider_type']
    search_fields = ['name', 'provider__business_name', 'description']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Service Information', {
            'fields': ('provider', 'name', 'description')
        }),
        ('Pricing & Duration', {
            'fields': ('price', 'duration')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at')
        }),
    )

@admin.register(ProviderDocument)
class ProviderDocumentAdmin(admin.ModelAdmin):
    list_display = ['provider', 'document_type', 'is_verified', 'uploaded_at']
    list_filter = ['document_type', 'is_verified', 'uploaded_at']
    search_fields = ['provider__business_name', 'provider__user__email']
    readonly_fields = ['uploaded_at']
    
    fieldsets = (
        ('Document Information', {
            'fields': ('provider', 'document_type', 'document_file')
        }),
        ('Verification', {
            'fields': ('is_verified', 'uploaded_at')
        }),
    )
    
    actions = ['verify_documents']
    
    def verify_documents(self, request, queryset):
        queryset.update(is_verified=True)
        self.message_user(request, f"{queryset.count()} documents have been verified.")
    verify_documents.short_description = "Verify selected documents"
