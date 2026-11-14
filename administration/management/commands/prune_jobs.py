"""Delete old finished background jobs.

Usage:
    python manage.py prune_jobs                # keep BACKGROUND_JOBS_RETENTION_DAYS
    python manage.py prune_jobs --days 7
"""

from django.core.management.base import BaseCommand

from administration.jobs import prune


class Command(BaseCommand):
    help = 'Delete finished background jobs older than the retention window'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days', type=int, default=None,
            help='Keep finished jobs newer than this many days.')

    def handle(self, *args, **options):
        deleted = prune(days=options['days'])
        self.stdout.write(self.style.SUCCESS(f'Deleted {deleted} job(s).'))
