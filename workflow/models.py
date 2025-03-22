from django.db import models
from workcentre.models import WorkCenter
# from .models import InspectionCheckpoint  

# Work Center Model
class WorkCenter(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

# Inspection Checkpoint Model (linked to Stage)
class InspectionCheckpoint(models.Model):
    checkpoint_name = models.CharField(max_length=255)
    inspection_criteria = models.TextField()
    tools_equipment_required = models.TextField()

    def __str__(self):
        return self.checkpoint_name
    @property
    def inspection_checkpoints(self):
        from . import InspectionCheckpoint  # delayed import inside method
        return self.inspectioncheckpoints.all()  # Assume there's a Many-to-Many field on Stage

# Stage Model (Updated to include inspection_checkpoints field as a list of IDs)
class Stage(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    assigned_work_center = models.ForeignKey(WorkCenter, on_delete=models.SET_NULL, null=True, blank=True)
    work_order = models.CharField(max_length=255, blank=True)
    duration = models.IntegerField(help_text="Duration in minutes")
    workflow = models.ForeignKey('Workflow', on_delete=models.CASCADE,related_name='workflow_stages')
    inspection_checkpoints = models.ManyToManyField(InspectionCheckpoint, blank=True)  # Many-to-many relation to Inspection Checkpoints
    
    def __str__(self):
        return self.name

# Workflow Model
class Workflow(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    product = models.ForeignKey('Product', on_delete=models.CASCADE ,related_name='workflows')  # Linking Workflow to Product
    assigned_work_center = models.ForeignKey(WorkCenter, on_delete=models.SET_NULL, null=True, blank=True)  # Link to WorkCenter
    stages = models.ManyToManyField('Stage', related_name='workflows', blank=True)
    def __str__(self):
        return self.name

# Product Model
class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=100, choices=[('Electronics', 'Electronics'), ('Furniture', 'Furniture'), ('Automotive', 'Automotive'), ('Clothing', 'Clothing'), ('Food', 'Food'), ('Other', 'Other')], default='Other')
    specifications = models.TextField()
    bom = models.ForeignKey('BOM', on_delete=models.CASCADE)
    workflow = models.ForeignKey(Workflow, on_delete=models.SET_NULL, null=True, blank=True ,related_name='products')  # Link Workflow
    
    def __str__(self):
        return self.name

# BOM Model
class BOM(models.Model):
    name = models.CharField(max_length=255)
    product_code = models.CharField(max_length=50)
    version = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=[('Approved', 'Approved'), ('Draft', 'Draft')], default='Draft')
    last_updated = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Component Model
class Component(models.Model):
    bom = models.ForeignKey(BOM, related_name='components', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    part_number = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=20)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name
