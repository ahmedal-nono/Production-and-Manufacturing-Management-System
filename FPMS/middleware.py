import re
from urllib.parse import urlparse

from django.conf import settings


class ApiRevalidateCacheMiddleware:
    """Let browsers keep API responses but revalidate them every time.

    Combined with Django's ConditionalGetMiddleware this turns repeated GET
    requests into cheap ``304 Not Modified`` responses, so the browser reuses
    the body it already has instead of downloading it again. Unchanged data is
    still verified with the server on each request, so a mutation can never be
    masked by a stale cache entry.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith('/api/'):
            response['Cache-Control'] = 'private, no-cache'
        return response


# Vite emits hashed assets such as ``index-DvRR04Yb.js``.
_HASHED_ASSET = re.compile(r'-[A-Za-z0-9_]{8,}\.(?:js|css|woff2?|webp|png|svg|jpg|jpeg)$')


class StaticCacheHeadersMiddleware:
    """Add long-lived cache headers for static assets.

    Hashed files are immutable and can be cached for a year; unhashed files
    get an hour. This makes a CDN (or the browser) safe to use in front of
    ``/static/``. When ``STATIC_URL`` points at a CDN the request never reaches
    Django, so the middleware simply does nothing.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        static_path = urlparse(settings.STATIC_URL).path or '/static/'
        self.static_prefix = static_path if static_path.endswith('/') else f'{static_path}/'

    def __call__(self, request):
        response = self.get_response(request)
        if (
            request.method == 'GET'
            and request.path.startswith(self.static_prefix)
            and response.status_code == 200
        ):
            if _HASHED_ASSET.search(request.path):
                response['Cache-Control'] = 'public, max-age=31536000, immutable'
            else:
                response['Cache-Control'] = 'public, max-age=3600'
        return response
