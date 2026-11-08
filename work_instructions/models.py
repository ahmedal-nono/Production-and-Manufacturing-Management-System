# models.py

from django.db import models
from workcentre.models import WorkCenter  # WorkCenter is in the workcentre app
# Assuming ProductionLine is in the workflow app
from workflow.models import ProductionLine


# Work Instruction Model
class WorkInstruction(models.Model):
    title = models.CharField(max_length=255)  # Title of the work instruction
    task_steps = models.TextField()  # Steps to complete the task
    tools_required = models.TextField()  # Tools required for the task
    materials_required = models.TextField()  # Materials required for the task
    step_description = models.TextField()  # Descriptions for each step
    status = models.CharField(
        max_length=50,
        choices=[('Not Started', 'Not Started'), ('In Progress',
                                                  'In Progress'), ('Completed', 'Completed')],
    )  # Status of the work instruction

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Work Instruction'
        verbose_name_plural = 'Work Instructions'


# Work Order Model
class WorkOrder(models.Model):
    name = models.CharField(max_length=255)  # Name of the work order
    # The quantity of items to be produced
    quantity_required = models.PositiveIntegerField()
    # Due date and time for completing the work order
    due_date = models.DateTimeField()
    priority = models.CharField(
        max_length=50, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')]
    )  # Priority of the work order
    # Work instruction linked to this work order
    work_instruction = models.ForeignKey(
        WorkInstruction, on_delete=models.CASCADE)
    production_line = models.ForeignKey(
        ProductionLine, on_delete=models.SET_NULL, null=True, blank=True
    )  # Linking work order to a production line
    production_order = models.ForeignKey(
        'workflow.ProductionOrder',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='work_orders'
    )

    def __str__(self):
        return f"Work Order {self.name} - {self.priority}"

    class Meta:
        verbose_name = 'Work Order'
        verbose_name_plural = 'Work Orders'
        indexes = [
            models.Index(fields=['production_order', 'due_date']),
            models.Index(fields=['production_line', 'due_date']),
            models.Index(fields=['priority', 'due_date']),
        ]


# Job Card Model (Generated from Work Order)
class JobCard(models.Model):
    work_order = models.ForeignKey(
        WorkOrder, on_delete=models.CASCADE, related_name='job_cards'
    )  # Linking the job card to a work order
    task_name = models.CharField(max_length=255)  # Name of the task
    required_tools = models.TextField()  # Tools required for the task
    required_materials = models.TextField()  # Materials required for the task
    status = models.CharField(
        max_length=50,
        choices=[('Not Started', 'Not Started'), ('In Progress',
                                                  'In Progress'), ('Completed', 'Completed')],
    )  # Status of the job card
    # The work center to which the job card is assigned
    assigned_to = models.ForeignKey(
        WorkCenter, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Job Card for {self.task_name}"

    class Meta:
        verbose_name = 'Job Card'
        verbose_name_plural = 'Job Cards'
        indexes = [
            models.Index(fields=['work_order', 'status']),
            models.Index(fields=['assigned_to', 'status']),
        ]
        