"""Small database-backed background job queue.

Jobs are rows in :class:`administration.models.BackgroundJob`. A worker
process (``python manage.py run_worker``) claims queued rows, runs the handler
and stores the result. This keeps slow operations (database backups, scheduled
tasks) out of the request/response cycle without adding a broker dependency.

Failures are retried with exponential backoff until ``max_attempts`` is
reached. Jobs left ``running`` by a crashed worker are recovered by
:func:`recover_stale` and either queued again or marked failed.

Set ``BACKGROUND_JOBS_EAGER=1`` to run jobs inline as soon as they are
enqueued (used by the demo and by tests).
"""

from __future__ import annotations

import os
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

from django.conf import settings
from django.db import connection
from django.db.models import F
from django.utils import timezone

from .models import BackgroundJob, BackupRecord


_HANDLERS = {}


def _max_attempts_default():
    return int(getattr(settings, 'BACKGROUND_JOBS_MAX_ATTEMPTS', 3))


def _retry_base_seconds():
    return float(getattr(settings, 'BACKGROUND_JOBS_RETRY_BASE', 2))


def _stale_after_seconds():
    return int(getattr(settings, 'BACKGROUND_JOBS_STALE_AFTER', 900))


def register(job_type):
    """Register a handler for ``job_type`` (decorator)."""

    def decorator(func):
        _HANDLERS[job_type] = func
        return func

    return decorator


def enqueue(job_type, payload=None, user=None, max_attempts=None, delay=0):
    """Create a queued job and return it.

    ``delay`` postpones the first run by that many seconds, which is handy for
    retrying work that failed because of a temporary condition.
    """
    now = timezone.now()
    return BackgroundJob.objects.create(
        job_type=job_type,
        payload=payload or {},
        created_by=user if getattr(user, 'pk', None) else None,
        max_attempts=max_attempts or _max_attempts_default(),
        available_at=now + timedelta(seconds=delay),
    )


def retry_delay_seconds(attempts):
    """Exponential backoff: 2s, 4s, 8s ... capped at five minutes."""
    return min(_retry_base_seconds() * (2 ** max(attempts - 1, 0)), 300)


def run_job(job):
    """Execute one job and persist its state, retrying retryable failures."""
    now = timezone.now()
    claimed = BackgroundJob.objects.filter(
        pk=job.pk, status='queued', available_at__lte=now).update(
        status='running', started_at=now, attempts=F('attempts') + 1)
    if not claimed:
        job.refresh_from_db()
        return job

    job.refresh_from_db()
    started = datetime.now()
    handler = _HANDLERS.get(job.job_type)
    try:
        if handler is None:
            raise LookupError(f'No handler registered for {job.job_type!r}')
        result = handler(job) or {}
    except Exception as exc:  # noqa: BLE001 - failures are stored for the UI
        job.error = str(exc)
        job.finished_at = timezone.now()
        if job.attempts < job.max_attempts:
            job.status = 'queued'
            job.available_at = timezone.now() + timedelta(
                seconds=retry_delay_seconds(job.attempts))
        else:
            job.status = 'failed'
        job.save(update_fields=[
            'status', 'error', 'available_at', 'finished_at',
        ])
    else:
        job.status = 'succeeded'
        job.result = result
        job.error = ''
        job.finished_at = timezone.now()
        job.save(update_fields=[
            'status', 'result', 'error', 'finished_at',
        ])

    # Keep the timestamp locally for logging/debugging.
    job.duration_seconds = (datetime.now() - started).total_seconds()
    return job


def recover_stale(age_seconds=None):
    """Re-queue jobs abandoned by a worker that stopped mid-run.

    A job is considered stale when it has been ``running`` longer than
    ``age_seconds`` (default ``BACKGROUND_JOBS_STALE_AFTER``). Jobs that still
    have attempts left go back to the queue; the rest are marked failed so the
    UI stops waiting for them.
    """
    limit_seconds = age_seconds if age_seconds is not None else _stale_after_seconds()
    threshold = timezone.now() - timedelta(seconds=limit_seconds)
    stale = BackgroundJob.objects.filter(
        status='running', started_at__lt=threshold)

    requeued = 0
    failed = 0
    for job in stale:
        note = f'Worker stopped before finishing (no update for {limit_seconds}s).'
        job.error = '\n'.join(filter(None, [job.error, note]))
        job.finished_at = timezone.now()
        if job.attempts < job.max_attempts:
            job.status = 'queued'
            job.available_at = timezone.now()
            requeued += 1
        else:
            job.status = 'failed'
            failed += 1
        job.save(update_fields=[
            'status', 'error', 'available_at', 'finished_at',
        ])
    return {'requeued': requeued, 'failed': failed}


def process_next():
    """Claim and run the oldest runnable job. Returns the job or ``None``."""
    job = BackgroundJob.objects.filter(
        status='queued', available_at__lte=timezone.now()
    ).order_by('available_at', 'created_at').first()
    if job is None:
        return None
    return run_job(job)


def run_pending(limit=None, recover=True):
    """Run up to ``limit`` runnable jobs and return how many were processed."""
    if recover:
        recover_stale()
    processed = 0
    while limit is None or processed < limit:
        job = process_next()
        if job is None:
            break
        processed += 1
    return processed


def prune(days=None):
    """Delete finished jobs older than ``days``. Returns the deleted count."""
    keep_days = days if days is not None else int(
        getattr(settings, 'BACKGROUND_JOBS_RETENTION_DAYS', 30))
    cutoff = timezone.now() - timedelta(days=keep_days)
    deleted, _ = BackgroundJob.objects.filter(
        status__in=['succeeded', 'failed'], created_at__lt=cutoff).delete()
    return deleted


def backup_path(filename):
    directory = Path(settings.MEDIA_ROOT) / 'backups'
    directory.mkdir(parents=True, exist_ok=True)
    return directory / filename


@register('system.echo')
def echo_handler(job):
    return {'echo': job.payload}


@register('backup.create')
def create_backup_handler(job):
    """Create a database backup and register it in ``BackupRecord``."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'fpms_backup_{timestamp}.sql'
    path = backup_path(filename)
    db_settings = settings.DATABASES['default']
    engine = db_settings['ENGINE']

    if engine.endswith('sqlite3'):
        connection.ensure_connection()
        with open(path, 'w', encoding='utf-8') as handle:
            for line in connection.connection.iterdump():
                handle.write(f'{line}\n')
    else:
        bin_path = os.environ.get('MARIADB_BIN_PATH', r'C:\Program Files\MariaDB 11.6\bin')
        mysqldump = os.environ.get(
            'MYSQLDUMP_PATH', os.path.join(bin_path, 'mysqldump.exe'))
        command = [
            mysqldump,
            f"--user={db_settings['USER']}",
            f"--password={db_settings['PASSWORD']}",
            f"--host={db_settings['HOST']}",
            f"--port={db_settings.get('PORT', '3306')}",
            db_settings['NAME'],
            f'--result-file={path}',
        ]
        env = os.environ.copy()
        env['PATH'] = f"{bin_path};{env['PATH']}"
        subprocess.run(
            command, check=True, env=env,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )

    file_size = os.path.getsize(path)
    created_by_id = job.payload.get('created_by_id')
    record = BackupRecord.objects.create(
        backup_file=f'backups/{filename}',
        created_by_id=created_by_id or None,
        file_size=file_size,
        is_automated=bool(job.payload.get('automated', False)),
    )
    return {
        'backup_id': record.id,
        'filename': filename,
        'file_path': str(path),
        'file_size': file_size,
    }
