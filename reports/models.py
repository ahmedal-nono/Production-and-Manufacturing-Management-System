from django.db import models
from workflow.models import ProductionLine
from workcentre.models import Workstation


class Issue(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    category = models.CharField(max_length=100)
    # Workflow/Workorder/JobCard reference
    affected_item = models.CharField(max_length=100)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Issue {self.id} - {self.category}"


class Report(models.Model):
    REPORT_TYPES = [  # Add your specific report types
        ('daily', 'Daily'),
        ('shift', 'Shift'),
        ('custom', 'Custom'),
    ]
    SHIFT_CHOICES = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('night', 'Night'),
    ]
    DATE_RANGE_CHOICES = [
        ('day', 'Day'),
        ('week', 'Week'),
        ('month', 'Month'),
        ('custom', 'Custom'),
    ]
    DEFECT_TYPES = [
        ('electrical', 'Electrical'),
        ('mechanical', 'Mechanical'),
        ('software', 'Software'),
    ]

    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    shift = models.CharField(max_length=20, choices=SHIFT_CHOICES)
    date_range_type = models.CharField(
        max_length=20, choices=DATE_RANGE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    production_line = models.ForeignKey(
        ProductionLine, on_delete=models.CASCADE)
    workstation = models.ForeignKey(Workstation, on_delete=models.CASCADE)
    defect_type = models.CharField(max_length=20, choices=DEFECT_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report {self.id} - {self.report_type}"
