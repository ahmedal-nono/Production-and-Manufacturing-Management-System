# administration/serializers.py
from rest_framework import serializers
from .models import User, Department, Role, HealthMetric, BackupConfig, BackupRecord, SystemSetting, ActivityLog, UserProfile, Notification, RumMetric, BackgroundJob
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        if not user.is_active:
            raise serializers.ValidationError("Account is inactive")
        return user
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
        # Handle department (free-text) when provided (PATCH may omit it)
        if 'department' in data:
            department_name = data.pop('department')
            if department_name:
                department, _ = Department.objects.get_or_create(
                    name=department_name,
                    defaults={'description': ''}
                )
                data['department_id'] = department.id
            else:
                data['department_id'] = None

        # Handle role: accept either the key ('production_manager') or the
        # display label ('Production Manager') so both create (select options)
        # and edit round-trip (GET returns the label) work.
        if 'role' in data:
            role_value = data.pop('role')
            if role_value:
                role_key = role_value if role_value in dict(Role.ROLE_CHOICES) else dict(
                    (label, key) for key, label in Role.ROLE_CHOICES).get(role_value)
                if not role_key:
                    raise serializers.ValidationError({
                        'role': f"Invalid role. Valid choices: {list(dict(Role.ROLE_CHOICES).keys())}"
                    })
                role, _ = Role.objects.get_or_create(
                    name=role_key,
                    defaults={'description': ''}
                )
                data['role_id'] = role.id
            else:
                data['role_id'] = None

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
        """Show department/role details in GET responses (role as display label)"""
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
        extra_kwargs = {
            'created_by': {'required': False, 'allow_null': True}
        }

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



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['profile_pic', 'security_question', 'security_answer']

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(min_length=8)


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'is_read', 'created_at', 'url',
                  'related_model', 'related_id']
        read_only_fields = ['id', 'created_at']


class RumMetricSerializer(serializers.ModelSerializer):
    ALLOWED_NAMES = {'LCP', 'CLS', 'INP', 'FCP', 'TTFB'}

    class Meta:
        model = RumMetric
        fields = ['id', 'name', 'value', 'rating', 'page_path', 'device',
                  'connection', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_name(self, value):
        if value not in self.ALLOWED_NAMES:
            raise serializers.ValidationError('Unsupported metric name')
        return value

    def validate_value(self, value):
        if value < 0 or value > 600000:
            raise serializers.ValidationError('Metric value out of range')
        return value


class BackgroundJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackgroundJob
        fields = ['id', 'job_type', 'status', 'result', 'error', 'attempts',
                  'max_attempts', 'available_at', 'created_at', 'started_at',
                  'finished_at']
        read_only_fields = fields
