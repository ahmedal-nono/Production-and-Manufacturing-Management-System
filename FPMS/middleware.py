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
