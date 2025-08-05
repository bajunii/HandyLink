from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Provider(models.Model):
    PROVIDER_TYPES = [
        ('individual', 'Individual'),
        ('company', 'Company'),
        ('freelancer', 'Freelancer'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('suspended', 'Suspended'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='provider_profile')
    business_name = models.CharField(max_length=255)
    provider_type = models.CharField(max_length=20, choices=PROVIDER_TYPES, default='individual')
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_verified = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.business_name} ({self.user.email})"

class ProviderService(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.provider.business_name}"

class ProviderDocument(models.Model):
    DOCUMENT_TYPES = [
        ('license', 'Business License'),
        ('certification', 'Certification'),
        ('insurance', 'Insurance'),
        ('id_proof', 'ID Proof'),
    ]
    
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    document_file = models.FileField(upload_to='provider_documents/')
    is_verified = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.provider.business_name} - {self.document_type}"


