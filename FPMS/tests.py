from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase, override_settings


class StaticCacheHeadersMiddlewareTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def _response_for(self, path):
        from FPMS.middleware import StaticCacheHeadersMiddleware

        middleware = StaticCacheHeadersMiddleware(
            lambda request: HttpResponse('ok'))
        return middleware(self.factory.get(path))

    @override_settings(STATIC_URL='/static/')
    def test_hashed_asset_is_cached_for_a_year(self):
        response = self._response_for('/static/assets/index-D21ncNCO.js')
        self.assertEqual(
            response['Cache-Control'],
            'public, max-age=31536000, immutable',
        )

    @override_settings(STATIC_URL='/static/')
    def test_unhashed_asset_is_cached_for_an_hour(self):
        response = self._response_for('/static/admin/base.css')
        self.assertEqual(response['Cache-Control'], 'public, max-age=3600')

    @override_settings(STATIC_URL='https://cdn.example.com/static/')
    def test_cdn_origin_still_matches_the_path(self):
        response = self._response_for('/static/assets/logo-a1b2c3d4.webp')
        self.assertEqual(
            response['Cache-Control'],
            'public, max-age=31536000, immutable',
        )

    @override_settings(STATIC_URL='/static/')
    def test_api_responses_are_not_touched(self):
        response = self._response_for('/api/reports/orders/status/')
        self.assertIsNone(response.get('Cache-Control'))
