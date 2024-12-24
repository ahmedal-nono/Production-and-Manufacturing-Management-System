from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Create default groups for user roles and assign permissions'

    def handle(self, *args, **kwargs):
        roles_permissions = {
            'production_manager': [
                'add_customuser', 'change_customuser', 'delete_customuser', 'view_customuser',
                'can_activate_user', 'can_deactivate_user'
            ],
            'production_planner': ['view_customuser'],
            'operator': ['view_customuser'],
            'supervisor': ['view_customuser'],
            'quality_control_manager': ['view_customuser', 'change_customuser'],
            'quality_control_inspector': ['view_customuser'],
        }

        for role, permissions in roles_permissions.items():
            group, created = Group.objects.get_or_create(name=role)
            for perm_codename in permissions:
                try:
                    perm = Permission.objects.get(codename=perm_codename)
                    group.permissions.add(perm)
                except Permission.DoesNotExist:
                    self.stdout.write(f'Permission \"{perm_codename}\" does not exist.')
            self.stdout.write(f'Group \"{role}\" updated with permissions.')
