from .models import ActivityLog
from django.contrib.auth import get_user_model

User = get_user_model()

def log_activity(
    user=None,
    action="",
    model="",
    object_id="",
    details=None,
    request=None
):
    """
    Simple function to log activities
    """
    if request and not user:
        user = request.user if request.user.is_authenticated else None
    
    activity = ActivityLog.objects.create(
        user=user,
        action=action,
        model=model,
        object_id=str(object_id) if object_id else "",
        details=details or {},
        ip_address=request.META.get('REMOTE_ADDR') if request else ""
    )
    return activity