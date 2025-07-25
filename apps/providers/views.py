from django.shortcuts import render
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Provider, ProviderService
from .serializers import (
    ProviderRegistrationSerializer, 
    ProviderSerializer,
    ProviderServiceSerializer
)

class ProviderRegistrationView(GenericAPIView):
    serializer_class = ProviderRegistrationSerializer
    
    @swagger_auto_schema(
        operation_summary='Register as a service provider',
        operation_description="""
        Allows verified users to register as service providers.
        
        **Requirements:**
        - User must be registered and email verified
        - User cannot already be a provider
        
        **Process:**
        1. Validates user email and verification status
        2. Creates provider profile
        3. Optionally adds initial services
        4. Sets status to 'pending' for admin approval
        """,
        responses={
            201: openapi.Response(
                description='Provider registered successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Provider registration successful. Your application is pending approval.'
                        ),
                        'provider_id': openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            example=1
                        )
                    }
                )
            ),
            400: openapi.Response(description='Validation errors')
        },
        tags=['Providers']
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            provider = serializer.save()
            return Response({
                'message': 'Provider registration successful. Your application is pending approval.',
                'provider_id': provider.id
            }, status=status.HTTP_201_CREATED)

class ProviderListView(ListAPIView):
    serializer_class = ProviderSerializer
    
    def get_queryset(self):
        return Provider.objects.filter(status='approved', is_verified=True).select_related('user')
    
    @swagger_auto_schema(
        operation_summary='List all approved providers',
        operation_description='Returns a list of all approved and verified service providers.',
        tags=['Providers']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ProviderDetailView(RetrieveAPIView):
    serializer_class = ProviderSerializer
    lookup_field = 'id'
    
    def get_queryset(self):
        return Provider.objects.filter(status='approved', is_verified=True).select_related('user')
    
    @swagger_auto_schema(
        operation_summary='Get provider details',
        operation_description='Returns detailed information about a specific provider.',
        tags=['Providers']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class MyProviderProfileView(GenericAPIView):
    serializer_class = ProviderSerializer
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary='Get my provider profile',
        operation_description='Returns the authenticated user\'s provider profile.',
        tags=['Providers']
    )
    def get(self, request):
        try:
            provider = request.user.provider_profile
            serializer = self.get_serializer(provider)
            return Response(serializer.data)
        except Provider.DoesNotExist:
            return Response({
                'message': 'You are not registered as a provider.'
            }, status=status.HTTP_404_NOT_FOUND)

class ProviderServicesView(ListAPIView):
    serializer_class = ProviderServiceSerializer
    
    def get_queryset(self):
        provider_id = self.kwargs['provider_id']
        return ProviderService.objects.filter(
            provider_id=provider_id, 
            provider__status='approved',
            is_active=True
        )
    
    @swagger_auto_schema(
        operation_summary='Get provider services',
        operation_description='Returns all active services offered by a specific provider.',
        tags=['Providers']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
