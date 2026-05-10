from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Locker


class LockerSerializer(serializers.ModelSerializer):
    """
    Locker object structure for frontend (Lab 9):
    {
      "id": 1,
      "locker_number": 1,
      "status": "Available",
      "rented_by": null,
      "rental_hours": 0,
      "created_at": "2024-01-01T12:00:00Z"
    }
    """
    rented_by = serializers.SerializerMethodField()
    
    class Meta:
        model = Locker
        fields = ['id', 'locker_number', 'status', 'rented_by', 'rental_hours', 'created_at']
    
    def get_rented_by(self, obj):
        """Return rented_by username or null"""
        if obj.rented_by:
            return obj.rented_by.username
        return None


class UserSerializer(serializers.ModelSerializer):
    """User authentication response"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class RegisterSerializer(serializers.Serializer):
    """User registration with validation"""
    username = serializers.CharField(max_length=150, min_length=3)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    
    def validate_username(self, value):
        """Validate username is unique and proper format"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken")
        if not value.replace('_', '').replace('-', '').isalnum():
            raise serializers.ValidationError("Username can only contain letters, numbers, hyphens, and underscores")
        return value
    
    def validate_email(self, value):
        """Validate email is unique"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email address is already registered")
        return value
    
    def validate_password(self, value):
        """Validate password strength"""
        if len(value) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters long")
        return value
    
    def create(self, validated_data):
        """Create user with hashed password"""
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    """User login with validation"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    
    def validate(self, data):
        """Validate credentials are provided"""
        if not data.get('username'):
            raise serializers.ValidationError("Username is required")
        if not data.get('password'):
            raise serializers.ValidationError("Password is required")
        return data