from django.db import models
from administration.models import User  # Use your custom user model


class Workcenter(models.Model):
    WORKCENTER_TYPES = [
        ('assembly', 'Assembly'),
        ('testing', 'Testing'),
        ('packaging', 'Packaging'),
        ('custom', 'Custom')
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=WORKCENTER_TYPES)
    location = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Workstation(models.Model):
    name = models.CharField(max_length=100)
    workcenter = models.ForeignKey(
        Workcenter, on_delete=models.CASCADE, related_name='workstations')
    status = models.CharField(max_length=20, choices=[
        ('idle', 'Idle'),
        ('active', 'Active'),
        ('maintenance', 'Under Maintenance')
    ], default='idle')
    capabilities = models.JSONField(default=dict)  # Store custom capabilities
    created_at = models.DateTimeField(auto_now_add=True)


class Equipment(models.Model):
    workstation = models.ForeignKey(
        Workstation, on_delete=models.CASCADE, related_name='equipment')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=50)


class Maintenance(models.Model):
    workstation = models.ForeignKey(Workstation, on_delete=models.CASCADE)
    scheduled_date = models.DateTimeField()
    completed = models.BooleanField(default=False)
    notes = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
