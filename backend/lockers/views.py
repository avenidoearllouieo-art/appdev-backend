from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Locker
from .serializers import LockerSerializer, UserSerializer, RegisterSerializer, LoginSerializer


# ===========================
# AUTHENTICATION ENDPOINTS
# ===========================

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def register(request):
    """
    POST /api/register/
    Register a new user
    
    Request:
    {
        "username": "john_doe",
        "email": "john@example.com",
        "password": "securepass123"
    }
    
    Response (201):
    {
        "success": true,
        "user": {...},
        "token": "abc123...",
        "message": "User registered successfully"
    }
    
    Response (400):
    {
        "success": false,
        "errors": {...},
        "message": "Registration failed"
    }
    """
    try:
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Create or get token for the new user
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'success': True,
                'user': UserSerializer(user).data,
                'token': token.key,
                'message': 'User registered successfully'
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'errors': serializer.errors,
            'message': 'Registration failed'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e),
            'message': 'An error occurred during registration'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def login(request):
    """
    POST /api/login/
    User login with token authentication
    
    Request:
    {
        "username": "john_doe",
        "password": "securepass123"
    }
    
    Response (200):
    {
        "success": true,
        "user": {...},
        "token": "abc123...",
        "message": "Login successful"
    }
    
    Response (400/401):
    {
        "success": false,
        "error": "Error message",
        "message": "Login failed"
    }
    """
    try:
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors,
                'message': 'Login failed'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        if not user:
            return Response({
                'success': False,
                'error': 'Invalid username or password',
                'message': 'Login failed'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Get or create token for authenticated user
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'success': True,
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e),
            'message': 'An error occurred during login'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ===========================
# LOCKER ENDPOINTS
# ===========================

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([AllowAny])
def lockers_list(request):
    """
    GET /api/lockers/
    Get all lockers with status
    
    Optional Authentication:
    - Authorization: Bearer <token> (optional, used to show user-specific data if needed)
    
    Response (200):
    {
        "success": true,
        "count": 10,
        "lockers": [...]
    }
    
    Response (500):
    {
        "success": false,
        "error": "Error message"
    }
    """
    try:
        lockers = Locker.objects.all()
        serializer = LockerSerializer(lockers, many=True)
        return Response({
            'success': True,
            'count': lockers.count(),
            'lockers': serializer.data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Failed to retrieve lockers: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'DELETE'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([AllowAny])
def locker_detail(request, id):
    """
    GET /api/lockers/{id}/
    Get a single locker by ID.
    
    DELETE /api/lockers/{id}/
    Delete a locker (requires authentication)
    """
    try:
        locker = Locker.objects.get(id=id)
    except Locker.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Locker not found',
            'message': 'Invalid locker ID'
        }, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'DELETE':
        if not request.user or not request.user.is_authenticated:
            return Response({
                'success': False,
                'error': 'Authentication required',
                'message': 'Authentication failed'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        locker.delete()
        return Response({
            'success': True,
            'message': 'Locker deleted successfully'
        }, status=status.HTTP_200_OK)
    
    serializer = LockerSerializer(locker)
    return Response({
        'success': True,
        'locker': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([AllowAny])
def rent_locker(request, id):
    """
    POST /api/lockers/{id}/rent/
    Rent a locker - assign to user and start timer
    
    Authentication Required:
    - Authorization: Bearer <token> (required for authenticated users)
    - Authorization: Token <token> (alternative format)
    
    Request:
    {
        "rental_hours": 2  # rental duration in hours (optional, default 1)
    }
    
    Response (200):
    {
        "success": true,
        "locker": {...},
        "message": "Locker rented successfully"
    }
    
    Response (400):
    {
        "success": false,
        "error": "Error message",
        "message": "Failed to rent locker"
    }
    
    Response (401):
    {
        "success": false,
        "error": "Authentication required",
        "message": "Authentication failed"
    }
    
    Response (404):
    {
        "success": false,
        "error": "Locker not found",
        "message": "Invalid locker ID"
    }
    """
    try:
        # Check if user is authenticated
        if not request.user or not request.user.is_authenticated:
            return Response({
                'success': False,
                'error': 'Authentication required',
                'message': 'Authentication failed'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Get locker
        try:
            locker = Locker.objects.get(id=id)
        except Locker.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Locker not found',
                'message': 'Invalid locker ID'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Check if locker is available
        if locker.status != "Available":
            return Response({
                'success': False,
                'error': f'Locker is not available (currently {locker.status})',
                'message': 'Failed to rent locker'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get and validate rental duration
        try:
            rental_hours = request.data.get('rental_hours', 1)
            rental_hours = int(rental_hours)
            
            if rental_hours <= 0:
                return Response({
                    'success': False,
                    'error': 'Rental hours must be a positive number',
                    'message': 'Failed to rent locker'
                }, status=status.HTTP_400_BAD_REQUEST)
        except (ValueError, TypeError):
            return Response({
                'success': False,
                'error': 'Rental hours must be a valid number',
                'message': 'Failed to rent locker'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Rent the locker to the authenticated user
        locker.rented_by = request.user
        locker.status = "In Use"
        locker.rental_hours = rental_hours
        locker.save()
        
        return Response({
            'success': True,
            'locker': LockerSerializer(locker).data,
            'message': 'Locker rented successfully'
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e),
            'message': 'An error occurred while renting the locker'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([AllowAny])
def release_locker(request, id):
    """
    POST /api/lockers/{id}/release/
    Release a locker - reset to available state
    
    Authentication Required:
    - Authorization: Bearer <token> (required)
    
    Request:
    {}
    
    Response (200):
    {
        "success": true,
        "locker": {...},
        "message": "Locker released successfully"
    }
    
    Response (400):
    {
        "success": false,
        "error": "Error message",
        "message": "Failed to release locker"
    }
    
    Response (401):
    {
        "success": false,
        "error": "Authentication required",
        "message": "Authentication failed"
    }
    
    Response (404):
    {
        "success": false,
        "error": "Locker not found",
        "message": "Invalid locker ID"
    }
    """
    try:
        # Check if user is authenticated
        if not request.user or not request.user.is_authenticated:
            return Response({
                'success': False,
                'error': 'Authentication required',
                'message': 'Authentication failed'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Get locker
        try:
            locker = Locker.objects.get(id=id)
        except Locker.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Locker not found',
                'message': 'Invalid locker ID'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Check if locker is in use
        if locker.status != "In Use":
            return Response({
                'success': False,
                'error': f'Locker is not in use (currently {locker.status})',
                'message': 'Failed to release locker'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Release the locker - reset to available
        locker.rented_by = None
        locker.status = "Available"
        locker.rental_hours = 0
        locker.save()
        
        return Response({
            'success': True,
            'locker': LockerSerializer(locker).data,
            'message': 'Locker released successfully'
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e),
            'message': 'An error occurred while releasing the locker'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)