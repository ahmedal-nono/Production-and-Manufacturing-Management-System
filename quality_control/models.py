from django.db import models
from work_instructions.models import WorkOrder, JobCard


class Inspection(models.Model):
    DECISION_CHOICES = [
        ('approve', 'Approve'),
        ('reject', 'Reject'),
        ('rework', 'Rework')
    ]
    SEVERITY_CHOICES = [
        ('critical', 'Critical'),
        ('major', 'Major'),
        ('minor', 'Minor')
    ]

    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    defect_type = models.CharField(max_length=100)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    affected_component = models.CharField(max_length=100)
    description = models.TextField()
    final_decision = models.CharField(max_length=20, choices=DECISION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class InspectionChecklist(models.Model):
    STATE_CHOICES = [
        ('pass', 'Pass'),
        ('fail', 'Fail')
    ]

    inspection = models.ForeignKey(
        Inspection, on_delete=models.CASCADE, related_name='checklist_items')
    job_card = models.ForeignKey(JobCard, on_delete=models.CASCADE)
    state = models.CharField(
        max_length=10, choices=STATE_CHOICES, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='inspections/', blank=True, null=True)


class ReworkRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]

    inspection = models.OneToOneField(
        Inspection, on_delete=models.CASCADE, related_name='rework_request')
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
