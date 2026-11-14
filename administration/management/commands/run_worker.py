"""Process queued background jobs.

Usage:
    python manage.py run_worker                # run forever, polling every N s
    python manage.py run_worker --once         # drain the queue and exit
    python manage.py run_worker --max-jobs 10  # process at most 10 then exit
    python manage.py run_worker --stale-after 300

The worker also recovers jobs abandoned by a previous crashed worker. Jobs
that fail are retried with exponential backoff (see ``administration.jobs``).
"""

import time

from django.conf import settings
from django.core.management.base import BaseCommand

from administration.jobs import recover_stale, run_pending


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
        parser.add_argument(
            '--stale-after', type=int,
            default=getattr(settings, 'BACKGROUND_JOBS_STALE_AFTER', 900),
            help='Re-queue jobs running for longer than this many seconds.')
        parser.add_argument(
            '--no-recover', action='store_true',
            help='Do not recover stale jobs on start-up.')

    def handle(self, *args, **options):
        once = options['once']
        max_jobs = options['max_jobs']
        interval = max(options['interval'], 0.1)
        stale_after = max(options['stale_after'], 1)
        recover = not options['no_recover']

        if recover:
            report = recover_stale(age_seconds=stale_after)
            if report['requeued'] or report['failed']:
                self.stdout.write(self.style.WARNING(
                    f"Recovered stale jobs: {report['requeued']} re-queued, "
                    f"{report['failed']} failed."))

        if once or max_jobs is not None:
            processed = run_pending(limit=max_jobs, recover=False)
            self.stdout.write(self.style.SUCCESS(
                f'Processed {processed} job(s).'))
            return

        self.stdout.write(self.style.SUCCESS(
            'Worker started. Press Ctrl+C to stop.'))
        try:
            while True:
                processed = run_pending(recover=False)
                if processed == 0:
                    time.sleep(interval)
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('Worker stopped.'))
