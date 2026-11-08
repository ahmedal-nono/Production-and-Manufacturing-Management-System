from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.http import JsonResponse
from django.conf import settings

from .context import set_current_request, clear_current_request


class ActivityLogMiddleware:
    """Expose the in-flight request to ``log_activity`` via thread-local storage.

    This lets model signals record *who* performed a change, even though the
    signal receivers do not have access to the request object.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        set_current_request(request)
        try:
            return self.get_response(request)
        finally:
            clear_current_request()


class JWTAutoRefreshMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Only process API requests that return 401
        if (request.path.startswith('/api/') and 
            response.status_code == 401 and
            'Authorization' in request.headers):
            
            try:
                refresh_token = request.COOKIES.get('refresh_token')
                if refresh_token:
                    refresh = RefreshToken(refresh_token)
                    new_access = str(refresh.access_token)
                    
                    # Update the response with new token
                    if isinstance(response, JsonResponse):
                        response.data['new_access_token'] = new_access
                    response.set_cookie(
                        'access_token', 
                        new_access,
                        httponly=True,
                        secure=not settings.DEBUG,
                        samesite='Lax'
                    )
            except TokenError:
                pass
                
        return response