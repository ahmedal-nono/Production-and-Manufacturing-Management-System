from rest_framework import serializers
from .models import (
    BOM,
    Product,
    Workflow,
    Stage,
    InspectionCheckpoint,
    Component,
    ProductionLine,
    ProductionOrder,
    Rescheduling
)
from workcentre.models import WorkCenter


class InspectionCheckpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionCheckpoint
        fields = [
            'id',
            'checkpoint_name',
            'inspection_criteria',
            'tools_equipment_required'
        ]


class StageSerializer(serializers.ModelSerializer):
    inspection_checkpoints = serializers.PrimaryKeyRelatedField(
        queryset=InspectionCheckpoint.objects.all(),
        many=True,
        required=False
    )
    workflow = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Stage
        fields = [
            'id',
            'name',
            'description',
            'assigned_work_center',
            'work_order',
            'duration',
            'inspection_checkpoints',
            'workflow'
        ]

    def create(self, validated_data):
        checkpoints = validated_data.pop('inspection_checkpoints', [])
        stage = Stage.objects.create(**validated_data)
        if checkpoints:
            stage.inspection_checkpoints.set(checkpoints)
        return stage


class WorkflowSerializer(serializers.ModelSerializer):
    stages = StageSerializer(many=True, required=False)
    assigned_work_center = serializers.PrimaryKeyRelatedField(
        queryset=WorkCenter.objects.all(),
        required=False,
        allow_null=True
    )
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all())

    class Meta:
        model = Workflow
        fields = [
            'id',
            'name',
            'description',
            'product',
            'assigned_work_center',
            'stages'
        ]

    def create(self, validated_data):
        stages_data = validated_data.pop('stages', [])
        workflow = Workflow.objects.create(**validated_data)
        for stage_data in stages_data:
            checkpoints = stage_data.pop('inspection_checkpoints', [])
            stage = Stage.objects.create(workflow=workflow, **stage_data)
            stage.inspection_checkpoints.set(checkpoints)
        return workflow

    def update(self, instance, validated_data):
        stages_data = validated_data.pop('stages', None)

        # تحديث الحقول الأساسية للـ Workflow
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if stages_data is not None:
            # حذف المراحل القديمة
            instance.stages.all().delete()

            # إنشاء المراحل الجديدة
            for stage_data in stages_data:
                checkpoints = stage_data.pop('inspection_checkpoints', [])
                stage = Stage.objects.create(workflow=instance, **stage_data)
                stage.inspection_checkpoints.set(checkpoints)

        return instance


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = [
            'id',
            'name',
            'part_number',
            'quantity',
            'unit',
            'unit_cost'
        ]


class BOMSerializer(serializers.ModelSerializer):
    components = ComponentSerializer(many=True)

    class Meta:
        model = BOM
        fields = [
            'id',
            'name',
            'product_code',
            'version',
            'status',
            'last_updated',
            'components'
        ]

    def create(self, validated_data):
        comps = validated_data.pop('components', [])
        bom = BOM.objects.create(**validated_data)
        for comp_data in comps:
            Component.objects.create(bom=bom, **comp_data)
        return bom

    def update(self, instance, validated_data):
        comps = validated_data.pop('components', [])

        # تحديث الحقول الأساسية
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # إزالة المكونات القديمة وإعادة إنشائها (يمكن لاحقًا تحسينه للتعديل الذكي)
        instance.components.all().delete()
        for comp_data in comps:
            Component.objects.create(bom=instance, **comp_data)

        return instance


class ProductSerializer(serializers.ModelSerializer):
    bom = serializers.PrimaryKeyRelatedField(queryset=BOM.objects.all())

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'sku',
            'category',
            'specifications',
            'bom'
        ]


class ProductionLineSerializer(serializers.ModelSerializer):
    work_centers = serializers.PrimaryKeyRelatedField(
        queryset=WorkCenter.objects.all(),
        many=True
    )

    class Meta:
        model = ProductionLine
        fields = [
            'id',
            'line_name',
            'capacity_limit',
            'oee_target',
            'status',
            'maintenance_schedule',
            'preferred_shift',
            'work_centers'
        ]

    def create(self, validated_data):
        wcs = validated_data.pop('work_centers', [])
        pl = ProductionLine.objects.create(**validated_data)
        pl.work_centers.set(wcs)
        return pl


class ProductionOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionOrder
        fields = [
            'id',
            'order_name',
            'priority',
            'product',
            'quantity',
            'start_date',
            'end_date',
            'production_line',
            'status'
        ]


class ReschedulingSerializer(serializers.ModelSerializer):
    production_order = serializers.PrimaryKeyRelatedField(
        queryset=ProductionOrder.objects.all()
    )

    class Meta:
        model = Rescheduling
        fields = [
            'id',
            'production_order',
            'new_start_time',
            'new_end_time',
            'reason_for_rescheduling',
            'notes'
        ]
