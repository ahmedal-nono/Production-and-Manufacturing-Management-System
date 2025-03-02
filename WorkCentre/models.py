from django.db import models

class WorkCenter(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='Active')
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Workstation(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='Active')
    capacity = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    work_center = models.ForeignKey(WorkCenter, on_delete=models.CASCADE, related_name='workstations')
    machines = models.JSONField(default=list)  # List of machine names
    tools = models.JSONField(default=list)  # List of tool names

    def __str__(self):
        return self.name

class Maintenance(models.Model):
    workstation = models.ForeignKey(Workstation, on_delete=models.CASCADE, related_name='maintenances')
    maintenance_date = models.DateField()
    maintenance_time = models.TimeField()
    recurrence = models.CharField(max_length=50, choices=[
        ('None', 'None'),
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
    ], default='None')
    description = models.TextField()
    staff_notes = models.TextField(blank=True, null=True)
    assigned_staff = models.JSONField(default=list)

    def __str__(self):
        return f"Maintenance for {self.workstation.name} on {self.maintenance_date}"
