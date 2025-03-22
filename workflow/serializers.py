from rest_framework import serializers
from .models import BOM, Product, Workflow, Stage, InspectionCheckpoint, Component
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
    bom = BOMSerializer()
    workflow = WorkflowSerializer()

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

# Workflow Serializer (Handles Workflow creation and stages)
