from django.contrib import admin
from .models import Review, ReviewResponse, ReviewHelpful

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'job', 'reviewer', 'provider', 'rating', 'quality_rating', 
        'timeliness_rating', 'would_recommend', 'is_verified', 'created_at'
    ]
    list_filter = [
        'rating', 'quality_rating', 'timeliness_rating', 'communication_rating', 
        'value_rating', 'would_recommend', 'is_verified', 'created_at'
    ]
    search_fields = [
        'title', 'content', 'reviewer__email', 'reviewer__first_name', 
        'reviewer__last_name', 'provider__business_name', 'job__title'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('job', 'reviewer', 'provider', 'title', 'content')
        }),
        ('Ratings', {
            'fields': ('rating', 'quality_rating', 'timeliness_rating', 'communication_rating', 'value_rating')
        }),
        ('Additional Information', {
            'fields': ('would_recommend', 'is_verified', 'photos')
        }),
        ('Provider Response', {
            'fields': ('provider_response', 'response_date'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('job', 'reviewer', 'provider')

@admin.register(ReviewResponse)
class ReviewResponseAdmin(admin.ModelAdmin):
    list_display = ['review', 'responder', 'created_at']
    list_filter = ['created_at']
    search_fields = ['review__title', 'responder__email', 'content']
    readonly_fields = ['created_at']

@admin.register(ReviewHelpful)
class ReviewHelpfulAdmin(admin.ModelAdmin):
    list_display = ['review', 'user', 'is_helpful', 'created_at']
    list_filter = ['is_helpful', 'created_at']
    search_fields = ['review__title', 'user__email']
    readonly_fields = ['created_at']
