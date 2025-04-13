# In any app's signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from administration.utils import log_activity

@receiver(post_save)
def log_save(sender, instance, created, **kwargs):
    if sender.__name__ not in ['ActivityLog', 'LogEntry']:  # Avoid logging logs
        action = 'create' if created else 'update'
        log_activity(
            user=getattr(instance, 'last_updated_by', None),
            action=action,
            model=sender.__name__,
            object_id=instance.id,
            # details={'changes': get_changes(instance)}  # Implement get_changes as neededpython manage.py makemigrations administration
        )

@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    if sender.__name__ not in ['ActivityLog', 'LogEntry']:
        log_activity(
            user=getattr(instance, 'deleted_by', None),
            action='delete',
            model=sender.__name__,
            object_id=instance.id
        )