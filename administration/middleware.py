# administration/middleware.py
from .models import ActivityLog
import json

class ActivityLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Skip logging for certain paths
        if request.path.startswith('/admin/') or request.path.startswith('/static/'):
            return response
        
        # Skip if user is not authenticated (except for login)
        if not request.user.is_authenticated and not request.path.endswith('/login/'):
            return response
        
        # Determine action type
        action = 'other'
        if request.method == 'POST':
            if request.path.endswith('/login/'):
                action = 'login'
            else:
                action = 'create'
        elif request.method == 'GET':
            action = 'read'
        elif request.method in ['PUT', 'PATCH']:
            action = 'update'
        elif request.method == 'DELETE':
            action = 'delete'
        
        # Get model name from URL if possible
        model = ''
        if hasattr(response, 'data') and isinstance(response.data, dict):
            model = response.data.get('model', '')
        
        # Create log entry
        ActivityLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            action=action,
            model=model,
            details={
                'path': request.path,
                'method': request.method,
                'status_code': response.status_code,
                'query_params': dict(request.GET),
                'data': request.data if hasattr(request, 'data') else {}
            },
            ip_address=self.get_client_ip(request)
        )
        
        return response
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip