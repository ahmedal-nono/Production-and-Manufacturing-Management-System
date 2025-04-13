# administration/utils.py
from .models import ActivityLog

def log_activity(user, action, model='', object_id='', details=None, ip_address=None):
    """
    Helper function to log activities from other apps
    """
    if details is None:
        details = {}
    
    ActivityLog.objects.create(
        user=user,
        action=action,
        model=model,
        object_id=str(object_id),
        details=details,
        ip_address=ip_address
    )