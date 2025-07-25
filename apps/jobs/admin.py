from django.contrib import admin
from .models import JobCategory, Job, JobApplication, JobReview, JobMessage

@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Category Information', {
            'fields': ('name', 'description', 'icon')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at')
        }),
    )

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'posted_by', 'category', 'status', 'urgency', 
        'budget_range', 'application_count', 'created_at'
    ]
    list_filter = [
        'status', 'urgency', 'category', 'is_remote', 'created_at'
    ]
    search_fields = [
        'title', 'description', 'location', 'posted_by__email', 
        'posted_by__first_name', 'posted_by__last_name'
    ]
    readonly_fields = [
        'application_count', 'budget_range', 'created_at', 'updated_at'
    ]
    
    fieldsets = (
        ('Job Information', {
            'fields': ('title', 'description', 'category', 'location')
        }),
        ('Budget & Timeline', {
            'fields': ('budget_min', 'budget_max', 'urgency', 'start_date', 'end_date', 'deadline')
        }),
        ('Assignment', {
            'fields': ('posted_by', 'assigned_to', 'status')
        }),
        ('Additional Details', {
            'fields': ('requirements', 'is_remote', 'images'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('application_count', 'budget_range'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_open', 'mark_as_completed', 'mark_as_cancelled']
    
    def mark_as_open(self, request, queryset):
        queryset.update(status='open')
        self.message_user(request, f"{queryset.count()} jobs marked as open.")
    mark_as_open.short_description = "Mark selected jobs as open"
    
    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
        self.message_user(request, f"{queryset.count()} jobs marked as completed.")
    mark_as_completed.short_description = "Mark selected jobs as completed"
    
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
        self.message_user(request, f"{queryset.count()} jobs marked as cancelled.")
    mark_as_cancelled.short_description = "Mark selected jobs as cancelled"

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'job', 'provider', 'bid_amount', 'estimated_duration', 
        'status', 'applied_at'
    ]
    list_filter = ['status', 'applied_at', 'job__category']
    search_fields = [
        'job__title', 'provider__business_name', 'provider__user__email'
    ]
    readonly_fields = ['applied_at', 'updated_at']
    
    fieldsets = (
        ('Application Details', {
            'fields': ('job', 'provider', 'bid_amount', 'estimated_duration')
        }),
        ('Proposal', {
            'fields': ('cover_letter',)
        }),
        ('Status & Dates', {
            'fields': ('status', 'applied_at', 'updated_at')
        }),
    )
    
    actions = ['accept_applications', 'reject_applications']
    
    def accept_applications(self, request, queryset):
        queryset.update(status='accepted')
        self.message_user(request, f"{queryset.count()} applications accepted.")
    accept_applications.short_description = "Accept selected applications"
    
    def reject_applications(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f"{queryset.count()} applications rejected.")
    reject_applications.short_description = "Reject selected applications"

@admin.register(JobReview)
class JobReviewAdmin(admin.ModelAdmin):
    list_display = [
        'job', 'reviewer', 'provider', 'rating', 
        'would_recommend', 'created_at'
    ]
    list_filter = ['rating', 'would_recommend', 'created_at']
    search_fields = [
        'job__title', 'reviewer__email', 'provider__business_name'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Review Information', {
            'fields': ('job', 'reviewer', 'provider')
        }),
        ('Rating & Feedback', {
            'fields': ('rating', 'comment', 'would_recommend')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(JobMessage)
class JobMessageAdmin(admin.ModelAdmin):
    list_display = ['job', 'sender', 'message_preview', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['job__title', 'sender__email', 'message']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Message Information', {
            'fields': ('job', 'sender', 'message', 'attachment')
        }),
        ('Status', {
            'fields': ('is_read', 'created_at')
        }),
    )
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message Preview'
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f"{queryset.count()} messages marked as read.")
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
        self.message_user(request, f"{queryset.count()} messages marked as unread.")
    mark_as_unread.short_description = "Mark selected messages as unread"
