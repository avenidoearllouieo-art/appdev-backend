from rest_framework.exceptions import AuthenticationFailed, PermissionDenied, NotAuthenticated
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler that returns consistent JSON responses
    for authentication, permission, and other API errors.
    """
    # Handle authentication and permission errors with consistent format
    if isinstance(exc, (NotAuthenticated, PermissionDenied, AuthenticationFailed)):
        return Response(
            {
                'success': False,
                'error': str(exc.detail),
                'message': 'Authentication failed'
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Handle other exceptions with consistent format
    from rest_framework.views import exception_handler
    response = exception_handler(exc, context)
    
    if response is not None:
        # Wrap existing DRF responses in our format
        response.data = {
            'success': False,
            'error': response.data,
            'message': 'An error occurred'
        }
    
    return response
