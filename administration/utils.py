from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv46_address

from .context import get_current_request
from .models import ActivityLog

try:
    from rest_framework_simplejwt.settings import api_settings as jwt_settings
    from rest_framework_simplejwt.tokens import AccessToken
except Exception:  # pragma: no cover - simplejwt is a hard dependency here
    AccessToken = None
    jwt_settings = None

User = get_user_model()


def _user_from_bearer(request):
    """Resolve the JWT bearer user for audit attribution.

    Django's ``request.user`` is still anonymous at signal time because DRF
    authenticates inside the view. Decoding the token here lets us still
    attribute the change to the real actor.
    """
    if AccessToken is None:
        return None
    # A single request usually triggers several model saves; decode once.
    cached = getattr(request, '_activity_log_actor', ...)
    if cached is not ...:
        return cached
    header = request.META.get('HTTP_AUTHORIZATION', '')
    actor = None
    if header.lower().startswith('bearer '):
        token = header.split(' ', 1)[1].strip()
        try:
            validated = AccessToken(token)
            user_id = validated[jwt_settings.USER_ID_CLAIM]
            actor = User.objects.filter(pk=user_id).first()
        except Exception:
            actor = None
    request._activity_log_actor = actor
    return actor


def _resolve_user(user, request):
    if user is not None:
        return user
    if request is None:
        return None
    request_user = getattr(request, 'user', None)
    if request_user is not None and request_user.is_authenticated:
        return request_user
    return _user_from_bearer(request)


def _client_ip(request):
    if request is None:
        return None
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = forwarded.split(',')[0].strip() if forwarded else request.META.get('REMOTE_ADDR')
    if not ip:
        return None
    try:
        validate_ipv46_address(ip)
    except ValidationError:
        return None
    return ip


def log_activity(
    user=None,
    action="",
    model="",
    object_id="",
    details=None,
    request=None
):
    """
    Create an audit entry.

    ``user`` may be omitted; the middleware-supplied current request is used
    to resolve the actor from the JWT bearer token (or the session) and to
    records the client IP / user agent.
    """
    if request is None:
        request = get_current_request()
    if user is None:
        user = _resolve_user(None, request)

    entry_details = dict(details or {})
    if request is not None:
        user_agent = request.META.get('HTTP_USER_AGENT')
        if user_agent and 'user_agent' not in entry_details:
            entry_details['user_agent'] = user_agent
        for key, value in (
            ('request_path', getattr(request, 'path', None)),
            ('request_method', getattr(request, 'method', None)),
        ):
            if value and key not in entry_details:
                entry_details[key] = value

    return ActivityLog.objects.create(
        user=user,
        action=action,
        model=model,
        object_id=str(object_id) if object_id else "",
        details=entry_details,
        ip_address=_client_ip(request),
    )
