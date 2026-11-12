"""Short-lived cache for expensive report aggregations.

Report endpoints build their payload with several joins and aggregates. A
small TTL absorbs repeated openings of the Reports screen without serving
stale data for long; writes to the underlying models invalidate the keys
immediately via ``reports.signals``.
"""

from django.conf import settings
from django.core.cache import cache

DEFAULT_TTL = getattr(settings, 'CACHE_TTL', 60)

PRODUCTION_PERFORMANCE_KEY = 'reports:production-performance:v1'
WORKFLOW_ANALYSIS_KEY = 'reports:workflow-analysis:v1'
ORDER_STATUS_KEY = 'reports:order-status:v1'
STAGE_DURATIONS_KEY = 'reports:stage-durations:v1:{workflow_id}'

ALL_KEYS = (
    PRODUCTION_PERFORMANCE_KEY,
    WORKFLOW_ANALYSIS_KEY,
    ORDER_STATUS_KEY,
)


def stage_durations_key(workflow_id=None):
    return STAGE_DURATIONS_KEY.format(workflow_id=workflow_id or 'all')


def cached(key, builder, ttl=None):
    """Return the cached value or build and store it."""
    value = cache.get(key)
    if value is None:
        value = builder()
        cache.set(key, value, ttl or DEFAULT_TTL)
    return value


def invalidate_report_caches(workflow_id=None):
    """Drop report caches after production data changes."""
    keys = list(ALL_KEYS)
    keys.append(stage_durations_key(None))
    if workflow_id is not None:
        keys.append(stage_durations_key(workflow_id))
    else:
        # We cannot enumerate workflow ids cheaply; bump the generic key and
        # let the short TTL handle per-workflow entries.
        pass
    cache.delete_many(keys)
