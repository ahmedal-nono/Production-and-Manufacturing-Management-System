import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

from django.core.handlers.wsgi import WSGIHandler
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


@unittest.skipUnless(
    importlib.util.find_spec('whitenoise'), 'whitenoise is not installed')
class WhiteNoiseStaticServingTests(SimpleTestCase):
    """End-to-end check: WhiteNoise serves /static/ with our cache policy."""

    def setUp(self):
        self.static_root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.static_root, True)
        assets = Path(self.static_root) / 'assets'
        assets.mkdir()
        (assets / 'index-abcdef12.js').write_text('console.log(1)')
        (assets / 'plain.js').write_text('console.log(2)')
        self.override = override_settings(STATIC_ROOT=self.static_root)
        self.override.enable()
        self.addCleanup(self.override.disable)
        self.handler = WSGIHandler()

    def _get(self, path):
        return self.handler.get_response(RequestFactory().get(path))

    def test_hashed_asset_is_served_as_immutable(self):
        response = self._get('/static/assets/index-abcdef12.js')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['Cache-Control'],
            'public, max-age=31536000, immutable',
        )

    def test_plain_asset_is_served_with_a_short_cache(self):
        response = self._get('/static/assets/plain.js')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Cache-Control'], 'public, max-age=3600')

    def test_missing_asset_is_a_404(self):
        response = self._get('/static/assets/missing.js')
        self.assertEqual(response.status_code, 404)
