from django.apps import AppConfig


class AdministrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'administration'

    def ready(self):
        # Register the audit-log receivers (post_save / post_delete).
        from . import signals  # noqa: F401
