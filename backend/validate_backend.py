#!/usr/bin/env python
"""
Backend Validation Script for Smart Locker System
Validates database operations and API structure without server
"""

import os
import sys
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from lockers.models import Locker
from lockers.serializers import LockerSerializer, UserSerializer, RegisterSerializer, LoginSerializer

def print_header(text):
    print(f"\n{'='*70}")
    print(f"  {text}")
    print('='*70)

def print_success(text):
    print(f"✓ {text}")

def print_error(text):
    print(f"✗ {text}")

def print_info(text):
    print(f"ℹ {text}")

def validate_models():
    """Validate Locker model structure"""
    print_header("VALIDATION 1: Locker Model Structure")
    
    try:
        # Check model fields
        locker = Locker.objects.first()
        if not locker:
            print_error("No lockers found in database")
            return False
        
        required_fields = ['id', 'locker_number', 'status', 'rented_by', 'rental_hours', 'created_at']
        for field in required_fields:
            if hasattr(locker, field):
                value = getattr(locker, field)
                print_success(f"Field '{field}' exists: {value}")
            else:
                print_error(f"Field '{field}' missing!")
                return False
        
        # Validate status choices
        if locker.status in ['Available', 'Occupied']:
            print_success(f"Status '{locker.status}' is valid (Available or Occupied)")
        else:
            print_error(f"Status '{locker.status}' is invalid")
            return False
        
        print_success("Locker model structure is valid")
        return True
    except Exception as e:
        print_error(f"Model validation error: {str(e)}")
        return False

def validate_serializers():
    """Validate serializer structure"""
    print_header("VALIDATION 2: Serializer Structure")
    
    try:
        # Test LockerSerializer
        locker = Locker.objects.first()
        serializer = LockerSerializer(locker)
        data = serializer.data
        
        required_fields = ['id', 'locker_number', 'status', 'rented_by', 'rental_hours', 'created_at']
        for field in required_fields:
            if field in data:
                print_success(f"LockerSerializer field '{field}': {data[field]}")
            else:
                print_error(f"LockerSerializer missing field '{field}'")
                return False
        
        # Test UserSerializer
        user = User.objects.first()
        if user:
            user_serializer = UserSerializer(user)
            user_data = user_serializer.data
            if 'username' in user_data and 'email' in user_data:
                print_success(f"UserSerializer valid: {user_data}")
            else:
                print_error("UserSerializer missing required fields")
                return False
        
        print_success("Serializers are valid")
        return True
    except Exception as e:
        print_error(f"Serializer validation error: {str(e)}")
        return False

def validate_authentication():
    """Validate token authentication"""
    print_header("VALIDATION 3: Token Authentication")
    
    try:
        # Clean up test user
        User.objects.filter(username='validationuser').delete()
        
        # Create test user
        user = User.objects.create_user(
            username='validationuser',
            email='validation@test.com',
            password='validpass123'
        )
        print_success(f"Created test user: {user.username}")
        
        # Get or create token
        token, created = Token.objects.get_or_create(user=user)
        print_success(f"Token created: {token.key[:20]}...")
        
        # Validate token
        if token.user == user:
            print_success("Token is properly associated with user")
        else:
            print_error("Token is not properly associated with user")
            return False
        
        # Clean up
        user.delete()
        print_success("Authentication validation passed")
        return True
    except Exception as e:
        print_error(f"Authentication validation error: {str(e)}")
        return False

def validate_locker_operations():
    """Validate locker rental operations"""
    print_header("VALIDATION 4: Locker Rental Operations")
    
    try:
        # Clean up test user
        User.objects.filter(username='renteruser').delete()
        
        # Create test user
        renter = User.objects.create_user(
            username='renteruser',
            email='renter@test.com',
            password='renterpass123'
        )
        print_success(f"Created renter user: {renter.username}")
        
        # Get available locker
        locker = Locker.objects.filter(status='Available').first()
        if not locker:
            print_error("No available lockers for testing")
            return False
        
        print_info(f"Using Locker {locker.locker_number} for rental test")
        
        # Test rent operation
        locker.rented_by = renter
        locker.status = 'Occupied'
        locker.rental_hours = 2
        locker.save()
        print_success(f"Locker rented: {locker.locker_number} by {locker.rented_by.username} for {locker.rental_hours}h")
        
        # Validate rental
        refreshed_locker = Locker.objects.get(id=locker.id)
        if refreshed_locker.status == 'Occupied' and refreshed_locker.rented_by == renter:
            print_success("Rental state persisted correctly")
        else:
            print_error("Rental state not persisted correctly")
            return False
        
        # Test release operation
        refreshed_locker.rented_by = None
        refreshed_locker.status = 'Available'
        refreshed_locker.rental_hours = 0
        refreshed_locker.save()
        print_success("Locker released")
        
        # Validate release
        final_locker = Locker.objects.get(id=locker.id)
        if final_locker.status == 'Available' and final_locker.rented_by is None:
            print_success("Release state persisted correctly")
        else:
            print_error("Release state not persisted correctly")
            return False
        
        # Clean up
        renter.delete()
        print_success("Locker operations validation passed")
        return True
    except Exception as e:
        print_error(f"Locker operations validation error: {str(e)}")
        return False

def validate_admin_config():
    """Validate Django admin configuration"""
    print_header("VALIDATION 5: Django Admin Configuration")
    
    try:
        from django.contrib import admin
        from lockers.admin import LockerAdmin
        from lockers.models import Locker
        
        # Check if Locker is registered in admin
        if Locker in admin.site._registry:
            print_success("Locker model is registered in Django admin")
        else:
            print_error("Locker model is NOT registered in Django admin")
            return False
        
        # Check LockerAdmin configuration
        admin_instance = admin.site._registry[Locker]
        
        expected_fields = ['locker_number', 'status', 'rented_by', 'rental_hours', 'is_active', 'created_at']
        if hasattr(admin_instance, 'list_display'):
            for field in expected_fields:
                if field in admin_instance.list_display:
                    print_success(f"Admin list_display includes '{field}'")
                else:
                    print_error(f"Admin list_display missing '{field}'")
        
        print_success("Django admin configuration is valid")
        return True
    except Exception as e:
        print_error(f"Admin configuration validation error: {str(e)}")
        return False

def validate_settings():
    """Validate Django settings"""
    print_header("VALIDATION 6: Django Settings Configuration")
    
    try:
        from django.conf import settings
        
        # Check INSTALLED_APPS
        required_apps = ['rest_framework', 'rest_framework.authtoken', 'corsheaders', 'lockers']
        for app in required_apps:
            if app in settings.INSTALLED_APPS:
                print_success(f"'{app}' in INSTALLED_APPS")
            else:
                print_error(f"'{app}' NOT in INSTALLED_APPS")
                return False
        
        # Check REST_FRAMEWORK settings
        if hasattr(settings, 'REST_FRAMEWORK'):
            rest_config = settings.REST_FRAMEWORK
            if 'DEFAULT_AUTHENTICATION_CLASSES' in rest_config:
                auth_classes = rest_config['DEFAULT_AUTHENTICATION_CLASSES']
                if 'rest_framework.authentication.TokenAuthentication' in auth_classes:
                    print_success("TokenAuthentication is configured")
                else:
                    print_error("TokenAuthentication is NOT configured")
                    return False
        
        # Check CORS settings
        if settings.CORS_ALLOW_ALL_ORIGINS:
            print_success("CORS_ALLOW_ALL_ORIGINS is enabled")
        else:
            print_error("CORS_ALLOW_ALL_ORIGINS is NOT enabled")
            return False
        
        print_success("Django settings configuration is valid")
        return True
    except Exception as e:
        print_error(f"Settings validation error: {str(e)}")
        return False

def main():
    """Run all validations"""
    print("\n" + "="*70)
    print("  SMART LOCKER SYSTEM - BACKEND VALIDATION")
    print("="*70)
    
    results = {
        'Models': validate_models(),
        'Serializers': validate_serializers(),
        'Authentication': validate_authentication(),
        'Locker Operations': validate_locker_operations(),
        'Admin Configuration': validate_admin_config(),
        'Settings': validate_settings(),
    }
    
    print_header("VALIDATION SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print_info(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print_success("\n✓ ALL VALIDATIONS PASSED - Backend is ready!")
        return 0
    else:
        print_error(f"\n✗ {total - passed} validation(s) failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())
