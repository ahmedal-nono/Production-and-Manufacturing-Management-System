"""Small database-backed background job queue.

Jobs are rows in :class:`administration.models.BackgroundJob`. A worker
process (``python manage.py run_worker``) claims queued rows, runs the handler
and stores the result. This keeps slow operations (database backups, scheduled
tasks) out of the request/response cycle without adding a broker dependency.

Set ``BACKGROUND_JOBS_EAGER=1`` to run jobs inline as soon as they are
enqueued (used by the demo and by tests).
"""

from __future__ import annotations

import os
import subprocess
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.db import connection
from django.utils import timezone

from .models import BackgroundJob, BackupRecord


_HANDLERS = {}


def register(job_type):
    """Register a handler for ``job_type`` (decorator)."""

    def decorator(func):
        _HANDLERS[job_type] = func
        return func

    return decorator


def enqueue(job_type, payload=None, user=None):
    """Create a queued job and return it."""
    return BackgroundJob.objects.create(
        job_type=job_type,
        payload=payload or {},
        created_by=user if getattr(user, 'pk', None) else None,
    )


def run_job(job):
    """Execute one job and persist its terminal state."""
    started = datetime.now()
    claimed = BackgroundJob.objects.filter(
        pk=job.pk, status='queued').update(
        status='running', started_at=timezone.now())
    if not claimed:
        job.refresh_from_db()
        return job

    job.refresh_from_db()
    handler = _HANDLERS.get(job.job_type)
    try:
        if handler is None:
            raise LookupError(f'No handler registered for {job.job_type!r}')
        result = handler(job) or {}
        job.status = 'succeeded'
        job.result = result
        job.error = ''
    except Exception as exc:  # noqa: BLE001 - failures are stored for the UI
        job.status = 'failed'
        job.error = str(exc)
    finally:
        job.finished_at = timezone.now()
        job.save(update_fields=['status', 'result', 'error', 'finished_at'])

    # Keep the timestamp locally for logging/debugging.
    job.duration_seconds = (datetime.now() - started).total_seconds()
    return job


def process_next():
    """Claim and run the oldest queued job. Returns the job or ``None``."""
    job = BackgroundJob.objects.filter(status='queued').order_by('created_at').first()
    if job is None:
        return None
    return run_job(job)


def run_pending(limit=None):
    """Run up to ``limit`` queued jobs and return how many were processed."""
    processed = 0
    while limit is None or processed < limit:
        job = process_next()
        if job is None:
            break
        processed += 1
    return processed


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
