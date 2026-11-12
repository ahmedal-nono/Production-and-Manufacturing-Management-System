# administration/management/commands/run_scheduled_backups.py
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone

from datetime import timedelta

from administration.jobs import enqueue, run_job
from administration.models import BackupConfig, BackupRecord


class Command(BaseCommand):
    help = (
        'Queue database backups for active schedules that are due. '
        'Run from cron/Task Scheduler alongside `manage.py run_worker`.'
    )

    def handle(self, *args, **options):
        now = timezone.localtime()
        admin_user = get_user_model().objects.filter(is_superuser=True).first()
        queued = 0

        for config in BackupConfig.objects.filter(is_active=True):
            due = (
                config.schedule_type == 'daily'
                or (config.schedule_type == 'weekly' and now.weekday() == 0)
                or (config.schedule_type == 'monthly' and now.day == 1)
            )
            if not due:
                continue
            if (now.hour, now.minute) != (
                    config.schedule_time.hour, config.schedule_time.minute):
                continue
            # Avoid running the same schedule twice in one minute.
            if config.last_run and config.last_run.date() == now.date():
                continue

            job = enqueue(
                'backup.create',
                {
                    'automated': True,
                    'created_by_id': admin_user.id if admin_user else None,
                    'retain_days': config.retain_days,
                },
                user=admin_user,
            )
            if settings.BACKGROUND_JOBS_EAGER:
                job = run_job(job)
                if job.status == 'succeeded':
                    self.cleanup_old_backups(config.retain_days)
            config.last_run = timezone.now()
            config.save(update_fields=['last_run'])
            queued += 1
            self.stdout.write(f'Queued backup job {job.id} ({config.schedule_type})')

        self.stdout.write(self.style.SUCCESS(f'Queued {queued} backup job(s).'))

    def cleanup_old_backups(self, retain_days):
        cutoff = timezone.now() - timedelta(days=retain_days)
        old_backups = BackupRecord.objects.filter(
            created_at__lt=cutoff,
            is_automated=True,
        )

        for backup in old_backups:
            try:
                backup.backup_file.delete(save=False)
                backup.delete()
            except Exception:
                pass
