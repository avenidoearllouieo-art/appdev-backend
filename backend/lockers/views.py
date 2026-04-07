from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Locker, UserProfile, ActivityLog
from .serializers import LockerSerializer, UserProfileSerializer, ActivityLogSerializer

# GET all lockers
@api_view(['GET'])
def get_lockers(request):
    lockers = Locker.objects.all()
    serializer = LockerSerializer(lockers, many=True)
    return Response(serializer.data)

# POST open locker
@api_view(['POST'])
def open_locker(request, id):
    locker = Locker.objects.get(id=id)
    locker.status = "In Use"
    locker.time_left = 60
    locker.save()
    
    # Log activity
    if request.user.is_authenticated:
        ActivityLog.objects.create(
            user=request.user,
            action=f"Opened locker {locker.number}",
            ip_address=get_client_ip(request)
        )
    
    return Response({"message": "Locker opened"})

# User Registration
@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    
    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=username, email=email, password=password)
    UserProfile.objects.create(user=user)
    
    ActivityLog.objects.create(
        user=user,
        action="User registration",
        ip_address=get_client_ip(request)
    )
    
    return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

# User Login
@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        
        ActivityLog.objects.create(
            user=user,
            action="User login",
            ip_address=get_client_ip(request)
        )
        
        return Response({"message": "Login successful"})
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip