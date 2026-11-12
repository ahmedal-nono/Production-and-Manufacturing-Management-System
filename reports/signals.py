from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from workflow.models import ProductionLine, ProductionOrder, Stage, Workflow

from .cache import invalidate_report_caches

# Report aggregates depend on these models; drop cached reports as soon as
# anything changes so the next request rebuilds the numbers.
_TRACKED_MODELS = (ProductionLine, ProductionOrder, Workflow, Stage)


def _invalidate(sender, instance, **kwargs):
    workflow_id = getattr(instance, 'workflow_id', None)
    invalidate_report_caches(workflow_id=workflow_id)


for _model in _TRACKED_MODELS:
    post_save.connect(
        _invalidate, sender=_model,
        dispatch_uid=f'reports.invalidate.save.{_model.__name__}',
        weak=False,
    )
    post_delete.connect(
        _invalidate, sender=_model,
        dispatch_uid=f'reports.invalidate.delete.{_model.__name__}',
        weak=False,
    )
