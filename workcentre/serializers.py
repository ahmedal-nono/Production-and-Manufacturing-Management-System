from rest_framework import serializers
from .models import WorkCenter, Workstation, Maintenance

class WorkCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkCenter
        fields = '__all__'

class WorkstationSerializer(serializers.ModelSerializer):
    work_center = serializers.PrimaryKeyRelatedField(
        queryset=WorkCenter.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Workstation
        fields = '__all__'

    def to_internal_value(self, data):
        if hasattr(data, 'get') and data.get('work_center') == '':
            data = {k: v for k, v in data.items() if k != 'work_center'}
        return super().to_internal_value(data)

class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = '__all__'