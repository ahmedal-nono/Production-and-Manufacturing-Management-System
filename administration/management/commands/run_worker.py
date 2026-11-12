"""Process queued background jobs.

Usage:
    python manage.py run_worker                # run forever, polling every N s
    python manage.py run_worker --once         # drain the queue and exit
    python manage.py run_worker --max-jobs 10  # process at most 10 then exit (with --once)
"""

import time

from django.conf import settings
from django.core.management.base import BaseCommand

from administration.jobs import run_pending


class Command(BaseCommand):
    help = 'Process queued background jobs'

    def add_arguments(self, parser):
        parser.add_argument(
            '--once', action='store_true',
            help='Process the current queue and exit (for cron/tests).')
        parser.add_argument(
            '--max-jobs', type=int, default=None,
            help='Maximum number of jobs to process before exiting.')
        parser.add_argument(
            '--interval', type=float,
            default=getattr(settings, 'BACKGROUND_JOBS_POLL_INTERVAL', 2),
            help='Seconds to sleep between polls in worker mode.')

    def handle(self, *args, **options):
        once = options['once']
        max_jobs = options['max_jobs']
        interval = max(options['interval'], 0.1)

        if once or max_jobs is not None:
            processed = run_pending(limit=max_jobs)
            self.stdout.write(self.style.SUCCESS(
                f'Processed {processed} job(s).'))
            return

        self.stdout.write(self.style.SUCCESS(
            'Worker started. Press Ctrl+C to stop.'))
        try:
            while True:
                processed = run_pending()
                if processed == 0:
                    time.sleep(interval)
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('Worker stopped.'))
