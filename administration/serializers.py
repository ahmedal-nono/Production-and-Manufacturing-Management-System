from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from .models import CustomUser
from .models import Backup

class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer for CustomUser model."""
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'fullname', 'email', 'contact_number', 'department', 'role', 'is_active', 'password']
        extra_kwargs = {
            'password': {'write_only': True}  # this my frends Ensure the password is not returned in API responses
        }

    def create(self, validated_data):
        """Handle user creation with password hashing."""
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        """Handle user updates with password hashing."""
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance

class GroupSerializer(serializers.ModelSerializer):
    """Serializer for Group model with permissions."""
    permissions = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Permission.objects.all()
    )

    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']

class PermissionSerializer(serializers.ModelSerializer):
    """Serializer for Permission model."""
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename']
        
class BackupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backup
        fields = ['id', 'name', 'file_path', 'created_at', 'status']
