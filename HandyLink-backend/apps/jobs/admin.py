from django.contrib import admin
from .models import JobCategory, Job, JobApplication, JobReview, JobMessage

@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'posted_by', 'category', 'status', 'urgency',
        'budget_min', 'budget_max', 'created_at'
    ]
    list_filter = ['status', 'urgency', 'category', 'is_remote', 'created_at']
    search_fields = ['title', 'description', 'posted_by__email', 'location']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category', 'posted_by')
        }),
        ('Budget & Location', {
            'fields': ('budget_min', 'budget_max', 'location', 'is_remote')
        }),
        ('Job Details', {
            'fields': ('urgency', 'status', 'assigned_to', 'deadline')
        }),
        ('Additional Information', {
            'fields': ('skills_required', 'attachments'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('posted_by', 'category', 'assigned_to')

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['job', 'provider', 'bid_amount', 'status', 'applied_at']
    list_filter = ['status', 'applied_at']
    search_fields = ['job__title', 'provider__business_name', 'cover_letter']
    readonly_fields = ['applied_at', 'updated_at']
    
    fieldsets = (
        ('Application Details', {
            'fields': ('job', 'provider', 'bid_amount', 'estimated_duration')
        }),
        ('Cover Letter', {
            'fields': ('cover_letter',)
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('applied_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(JobReview)
class JobReviewAdmin(admin.ModelAdmin):
    list_display = ['job', 'reviewer', 'provider', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['job__title', 'reviewer__email', 'provider__business_name', 'comment']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Review Details', {
            'fields': ('job', 'reviewer', 'provider', 'rating')
        }),
        ('Comment', {
            'fields': ('comment',)
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

@admin.register(JobMessage)
class JobMessageAdmin(admin.ModelAdmin):
    list_display = ['job', 'sender', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['job__title', 'sender__email', 'message']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Message Details', {
            'fields': ('job', 'sender', 'message', 'is_read')
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
