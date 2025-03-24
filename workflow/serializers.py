from rest_framework import serializers
from .models import BOM, Product, Workflow, Stage, InspectionCheckpoint, Component
from .models import Product, ProductionLine, ProductionOrder, Rescheduling
from workcentre.models import WorkCenter  
from .models import Product

class InspectionCheckpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionCheckpoint
        fields = ['id', 'checkpoint_name', 'inspection_criteria', 'tools_equipment_required']

class StageSerializer(serializers.ModelSerializer):
    inspection_checkpoints = serializers.PrimaryKeyRelatedField(queryset=InspectionCheckpoint.objects.all(), many=True)  # Handle Inspection Checkpoints

    class Meta:
        model = Stage
        fields = ['id', 'name', 'description', 'assigned_work_center', 'work_order', 'duration', 'workflow', 'inspection_checkpoints']

    def create(self, validated_data):
        inspection_checkpoints_data = validated_data.pop('inspection_checkpoints', [])
        stage = Stage.objects.create(**validated_data)
        for checkpoint in inspection_checkpoints_data:
            stage.inspection_checkpoints.add(checkpoint)
        return stage

class WorkflowSerializer(serializers.ModelSerializer):
    stages = StageSerializer(many=True)  # Handle multiple stages
    assigned_work_center = serializers.PrimaryKeyRelatedField(queryset=WorkCenter.objects.all(), required=False)  # Handle assigned_work_center as a select field
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())  # Handle product as a select field

    class Meta:
        model = Workflow
        fields = ['id', 'name', 'description', 'product', 'assigned_work_center', 'stages']  # Include all necessary fields

    def create(self, validated_data):
        stages_data = validated_data.pop('stages')  # Extract stages data
        workflow = Workflow.objects.create(**validated_data)  # Create the workflow
        
        for stage_data in stages_data:
            Stage.objects.create(workflow=workflow, **stage_data)  # Create stages and link to workflow
        
        return workflow



# BOM Serializer (Handles BOM with its components)
class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ['id', 'name', 'part_number', 'quantity', 'unit', 'unit_cost']

class BOMSerializer(serializers.ModelSerializer):
    components = ComponentSerializer(many=True)

    class Meta:
        model = BOM
        fields = ['id', 'name', 'product_code', 'version', 'status', 'created_by', 'last_updated', 'components']

    def create(self, validated_data):
        components_data = validated_data.pop('components')
        bom = BOM.objects.create(**validated_data)
        for component_data in components_data:
            Component.objects.create(bom=bom, **component_data)
        return bom

# Product Serializer (Handles Product creation and updating)
class ProductSerializer(serializers.ModelSerializer):
    bom =serializers.PrimaryKeyRelatedField(queryset=Workflow.objects.all())
    workflow = serializers.PrimaryKeyRelatedField(queryset=BOM.objects.all())

    class Meta:
        model = Product
        fields = ['id', 'name', 'sku', 'category', 'specifications', 'bom', 'workflow']
    
    def create(self, validated_data):
        bom_data = validated_data.pop('bom')
        workflow_data = validated_data.pop('workflow')

        # Create BOM and Workflow first
        bom = BOM.objects.create(**bom_data)
        workflow = Workflow.objects.create(**workflow_data)

        # Create the Product and associate it with the BOM and Workflow
        product = Product.objects.create(bom=bom, workflow=workflow, **validated_data)

        return product

    def update(self, instance, validated_data):
        bom_data = validated_data.pop('bom')
        workflow_data = validated_data.pop('workflow')

        # Update the BOM and Workflow
        instance.bom.name = bom_data.get('name', instance.bom.name)
        instance.workflow.name = workflow_data.get('name', instance.workflow.name)

        instance.save()

        return instance

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'sku', 'category', 'specifications']

# serializers.py
class ProductionLineSerializer(serializers.ModelSerializer):
    work_centers = serializers.CharField(write_only=True)  # Accepting work center names
    
    class Meta:
        model = ProductionLine
        fields = ['id', 'line_name', 'capacity_limit', 'maintenance_schedule', 'preferred_shift', 'status', 'oee_target', 'work_centers']
    
    def create(self, validated_data):
        work_centers_data = validated_data.pop('work_centers', [])
        production_line = ProductionLine.objects.create(**validated_data)
        
        # Process work centers by name
        for work_center_name in work_centers_data:
            work_center = WorkCenter.objects.get(name=work_center_name)
            production_line.work_centers.add(work_center)
        
        return production_line
# serializers.py
class ProductionOrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = ProductionOrder
        fields = ['id', 'order_name', 'priority', 'product', 'quantity', 'start_date', 'end_date', 'production_line', 'status']

    def create(self, validated_data):
        product_name = validated_data.pop('product_name', None)
        if product_name:
            product = Product.objects.get(name=product_name)
            validated_data['product'] = product
        production_order = ProductionOrder.objects.create(**validated_data)
        return production_order


# serializers.py
class ReschedulingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rescheduling
        fields = ['id', 'production_order', 'new_start_time', 'new_end_time', 'reason_for_rescheduling', 'notes']



