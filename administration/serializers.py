# administration/serializers.py
from rest_framework import serializers
from .models import User, Department, Role, HealthMetric, BackupConfig, BackupRecord, SystemSetting, ActivityLog
from django.contrib.auth.hashers import make_password

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    department = serializers.CharField(write_only=True)  # Accepts free-text department
    role = serializers.CharField(write_only=True)  # Accepts role choice value
    
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'contact_number', 
                 'department', 'role', 'account_status', 'password']
        read_only_fields = ['id', 'account_status']
        extra_kwargs = {
            'password': {'write_only': True},
            'account_status': {'read_only': True}  # Only changed via activate/deactivate endpoints
        }  

    def validate(self, data):
        # Handle department (free-text)
        department_name = data.pop('department')
        department, _ = Department.objects.get_or_create(
            name=department_name,
            defaults={'description': ''}
        )
        data['department_id'] = department.id
        
        # Handle role (must match ROLE_CHOICES)
        role_name = data.pop('role')
        if role_name not in dict(Role.ROLE_CHOICES):
            raise serializers.ValidationError({
                'role': f"Invalid role. Valid choices: {list(dict(Role.ROLE_CHOICES).keys())}"
            })
        role, _ = Role.objects.get_or_create(
            name=role_name,
            defaults={'description': ''}
        )
        data['role_id'] = role.id
        
        return data

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    # def validate(self, data):
    #     # Prevent non-admins from changing account_status
    #     if 'account_status' in data and not self.context['request'].user.is_staff:
    #         raise serializers.ValidationError("Only admins can change account status")
    #     return data
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        """Show department/role details in GET responses"""
        representation = super().to_representation(instance)
        representation['department'] = instance.department.name if instance.department else None
        representation['role'] = instance.role.get_name_display() if instance.role else None
        return representation

class BackupConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupConfig
        fields = '__all__'

class BackupRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupRecord
        fields = '__all__'
        read_only_fields = ['backup_file', 'created_at', 'file_size']

class SystemSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemSetting
        fields = '__all__'

class HealthMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthMetric
        fields = '__all__'

class ActivityLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = ActivityLog
        fields = '__all__'