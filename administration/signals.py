"""Global receivers that write an ActivityLog row for every model change.

The actor (user) is not passed in by the receiver: ``log_activity`` resolves
it from the request stored in thread-local storage by
``ActivityLogMiddleware`` (session user or JWT bearer token).
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from administration.utils import log_activity

# Framework apps whose bookkeeping tables should not pollute the audit trail.
IGNORED_APP_LABELS = {
    'admin',
    'auth',
    'contenttypes',
    'sessions',
    'migrations',
    'authtoken',
}

# Never log the audit trail itself (would recurse on every insert).
IGNORED_MODELS = {'ActivityLog', 'LogEntry'}


def _should_log(sender):
    if sender.__name__ in IGNORED_MODELS:
        return False
    app_label = getattr(getattr(sender, '_meta', None), 'app_label', '')
    return app_label not in IGNORED_APP_LABELS


@receiver(post_save)
def log_save(sender, instance, created, **kwargs):
    if not _should_log(sender):
        return
    log_activity(
        user=getattr(instance, 'last_updated_by', None),
        action='create' if created else 'update',
        model=sender.__name__,
        object_id=instance.pk,
    )


@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    if not _should_log(sender):
        return
    log_activity(
        user=getattr(instance, 'deleted_by', None),
        action='delete',
        model=sender.__name__,
        object_id=instance.pk,
    )
