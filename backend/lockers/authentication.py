from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed


class BearerTokenAuthentication(TokenAuthentication):
    """
    Custom authentication class that accepts both 'Token' and 'Bearer' prefixes
    for the Authorization header. This ensures compatibility with various clients
    and prevents authentication issues when renting lockers.
    
    Supports:
    - Authorization: Bearer <token>
    - Authorization: Token <token>
    """
    keyword = 'Bearer'
    
    def authenticate(self, request):
        """
        Authenticate request using Bearer or Token prefix in Authorization header.
        Returns (user, token) tuple on success, None if no auth header, or raises AuthenticationFailed.
        """
        auth = request.META.get('HTTP_AUTHORIZATION', '').split()
        
        if len(auth) == 2:
            if auth[0].lower() == 'bearer':
                # This is a Bearer token
                try:
                    token = Token.objects.get(key=auth[1])
                    return (token.user, token)
                except Token.DoesNotExist:
                    raise AuthenticationFailed('Invalid token.')
            elif auth[0].lower() == 'token':
                # This is a Token format
                try:
                    token = Token.objects.get(key=auth[1])
                    return (token.user, token)
                except Token.DoesNotExist:
                    raise AuthenticationFailed('Invalid token.')
        
        # If no proper auth header, return None (allows AllowAny to work)
        return None
