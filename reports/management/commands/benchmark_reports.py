"""Measure report latency with and without the report cache.

Runs the same report endpoints through Django's test client twice: once with a
cold cache (every run clears it, so the aggregations hit the database) and once
with a warm cache. Prints the median of each so the gain is measured instead of
assumed.

Usage:
    python manage.py benchmark_reports
    python manage.py benchmark_reports --runs 10 --email admin@demo.com
    python manage.py benchmark_reports --json benchmark.json
"""

import json
import statistics
import time

from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError
from django.test import Client, override_settings

from administration.models import User

ENDPOINTS = [
    ('production performance', '/api/reports/production/performance/'),
    ('workflow analysis', '/api/reports/workflow/analysis/'),
    ('order status', '/api/reports/orders/status/'),
    ('stage durations', '/api/reports/stages/durations/'),
]


class Command(BaseCommand):
    help = 'Measure report latency with a cold and a warm cache'

    def add_arguments(self, parser):
        parser.add_argument(
            '--runs', type=int, default=5,
            help='Number of requests per endpoint for each cache state.')
        parser.add_argument(
            '--email', default=None,
            help='User used for the requests (defaults to an admin).')
        parser.add_argument(
            '--json', dest='json_path', default=None,
            help='Write the measurements to this JSON file.')

    def handle(self, *args, **options):
        runs = max(1, options['runs'])
        user = self._pick_user(options['email'])
        token = self._token_for(user)
        headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}

        # The test client uses ``testserver``; allow it without touching the
        # project's configured hosts.
        with override_settings(ALLOWED_HOSTS=['testserver', 'localhost']):
            client = Client()
            results = []
            for label, path in ENDPOINTS:
                cold = self._measure(client, headers, path, runs, clear=True)
                warm = self._measure(client, headers, path, runs, clear=False)
                results.append({
                    'endpoint': label,
                    'path': path,
                    'cold_ms': round(statistics.median(cold), 2),
                    'warm_ms': round(statistics.median(warm), 2),
                    'speedup': round(
                        statistics.median(cold) / statistics.median(warm), 2)
                    if statistics.median(warm) else None,
                    'runs': runs,
                })

        self._print_table(results, user)

        if options['json_path']:
            with open(options['json_path'], 'w', encoding='utf-8') as handle:
                json.dump(
                    {'user': user.email, 'runs': runs, 'results': results},
                    handle, indent=2)
            self.stdout.write(self.style.SUCCESS(
                f'Wrote {options["json_path"]}'))

    def _pick_user(self, email):
        if email:
            try:
                return User.objects.get(email=email)
            except User.DoesNotExist:
                raise CommandError(f'No user with email {email!r}')
        admin = User.objects.filter(role__name='admin').first()
        admin = admin or User.objects.filter(is_superuser=True).first()
        if admin is None:
            raise CommandError(
                'No admin user found; pass --email or run the demo seed.')
        return admin

    def _token_for(self, user):
        from rest_framework_simplejwt.tokens import AccessToken

        return str(AccessToken.for_user(user))

    def _measure(self, client, headers, path, runs, clear):
        timings = []
        for _ in range(runs):
            if clear:
                cache.clear()
            started = time.perf_counter()
            response = client.get(path, **headers)
            timings.append((time.perf_counter() - started) * 1000)
            if response.status_code != 200:
                raise CommandError(
                    f'{path} returned {response.status_code}: '
                    f'{response.content[:200]!r}')
        return timings

    def _print_table(self, results, user):
        self.stdout.write(f'User: {user.email}')
        self.stdout.write(
            f'{"endpoint":<24}{"cold (ms)":>12}{"warm (ms)":>12}{"speedup":>10}')
        for row in results:
            self.stdout.write(
                f'{row["endpoint"]:<24}{row["cold_ms"]:>12}'
                f'{row["warm_ms"]:>12}{str(row["speedup"]):>10}')
