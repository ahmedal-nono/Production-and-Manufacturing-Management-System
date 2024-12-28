from django.contrib.auth.models import AbstractUser, Group
from django.db import models

class CustomUser(AbstractUser):
    fullname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(
        max_length=50,
        choices=[
            ('production_manager', 'Production Manager'),
            ('production_planner', 'Production Planner'),
            ('operator', 'Operator'),
            ('supervisor', 'Supervisor'),
            ('quality_control_manager', 'Quality Control Manager'),
            ('quality_control_inspector', 'Quality Control Inspector')
        ]
    )
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Save the user object first to ensure it has an ID
        super().save(*args, **kwargs)

        # Assign the user to the appropriate group based on their role
        if self.role:
            group, _ = Group.objects.get_or_create(name=self.role)
            self.groups.add(group)  # Add the group to the user after the user is saved

    class Meta:
        permissions = [
            ("can_activate_user", "Can activate a user"),
            ("can_deactivate_user", "Can deactivate a user"),
        ]
