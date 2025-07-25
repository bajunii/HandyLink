from rest_framework import serializers
from .models import Provider, ProviderService, ProviderDocument
from apps.users.serializers import UserSerializer

class ProviderDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderDocument
        fields = ['id', 'document_type', 'document_file', 'is_verified', 'uploaded_at']
        read_only_fields = ['is_verified', 'uploaded_at']

class ProviderServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderService
        fields = ['id', 'name', 'description', 'price', 'duration', 'is_active', 'created_at']
        read_only_fields = ['created_at']

class ProviderRegistrationSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(write_only=True)
    services = ProviderServiceSerializer(many=True, required=False)
    
    class Meta:
        model = Provider
        fields = [
            'user_email', 'business_name', 'provider_type', 'description', 
            'website', 'phone_number', 'address', 'services'
        ]
    
    def validate_user_email(self, value):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        try:
            user = User.objects.get(email=value)
            if not user.is_verified:
                raise serializers.ValidationError("User email must be verified before becoming a provider.")
            if hasattr(user, 'provider_profile'):
                raise serializers.ValidationError("User is already registered as a provider.")
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
    
    def create(self, validated_data):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        user_email = validated_data.pop('user_email')
        services_data = validated_data.pop('services', [])
        
        user = User.objects.get(email=user_email)
        provider = Provider.objects.create(user=user, **validated_data)
        
        for service_data in services_data:
            ProviderService.objects.create(provider=provider, **service_data)
        
        return provider

class ProviderSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.SerializerMethodField()
    services = ProviderServiceSerializer(many=True, read_only=True)
    documents = ProviderDocumentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Provider
        fields = [
            'id', 'user_email', 'user_name', 'business_name', 'provider_type', 'description',
            'website', 'phone_number', 'address', 'status', 'is_verified',
            'rating', 'total_reviews', 'services', 'documents',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['status', 'is_verified', 'rating', 'total_reviews', 'created_at', 'updated_at']
    
    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip()