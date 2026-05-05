from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from .models import Locker, UserProfile, ActivityLog
from .serializers import LockerSerializer, UserProfileSerializer, ActivityLogSerializer

# GET all lockers or POST to create a new locker
@csrf_exempt
@api_view(['GET', 'POST'])
def get_lockers(request):
    if request.method == 'GET':
        lockers = Locker.objects.all()
        serializer = LockerSerializer(lockers, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = LockerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

# DELETE locker
@api_view(['DELETE'])
def delete_locker(request, id):
    try:
        locker = Locker.objects.get(id=id)
        locker_number = locker.number
        locker.delete()
        
        # Log activity
        if request.user.is_authenticated:
            ActivityLog.objects.create(
                user=request.user,
                action=f"Deleted locker {locker_number}",
                ip_address=get_client_ip(request)
            )
        
        return Response({"message": f"Locker {locker_number} deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Locker.DoesNotExist:
        return Response({"error": "Locker not found"}, status=status.HTTP_404_NOT_FOUND)

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