# administration/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Role(models.Model):
    ROLE_CHOICES = [
        ('quality_control_inspector', 'Quality Control Inspector'),
        ('quality_control_manager', 'Quality Control Manager'),
        ('supervisor', 'Supervisor'),
        ('operator', 'Operator'),
        ('production_planner', 'Production Planner'),
        ('production_manager', 'Production Manager'),
        ('admin', 'Admin'),
    ]
    
    name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True)
    permissions = models.JSONField(default=list)  # Store permission codes
    
    def __str__(self):
        return self.get_name_display()
class UserManager(BaseUserManager):
    def get_by_natural_key(self, username):
        """Allow authentication via email instead of username"""
        return self.get(email=username)
    
    def create_user(self, email, full_name, password=None, **extra_fields):
        """Create and save a regular User with email and password"""
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, full_name, password=None, **extra_fields):
        """Create and save a SuperUser with email and password"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        return self.create_user(email, full_name, password, **extra_fields)
class User(AbstractUser):
    # Custom fields
    full_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20, blank=True)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, blank=True)
    account_status = models.BooleanField(default=True)
    
    # Authentication fields
    username = None  # Remove username field
    email = models.EmailField(unique=True)
    
    # Required for custom user model
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    
    # Assign the custom manager
    objects = UserManager()
    
    def __str__(self):
        return self.full_name
    
    class Meta:
        # Ensures proper table naming and model identification
        db_table = 'administration_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    security_question = models.CharField(max_length=200, blank=True)
    security_answer = models.CharField(max_length=200, blank=True)

# administration/models.py
class BackupConfig(models.Model):
    SCHEDULE_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    
    schedule_type = models.CharField(max_length=10, choices=SCHEDULE_CHOICES)
    schedule_time = models.TimeField()
    last_run = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    retain_days = models.PositiveIntegerField(default=7)
    
    def __str__(self):
        return f"{self.get_schedule_type_display()} at {self.schedule_time}"

class BackupRecord(models.Model):
    backup_file = models.FileField(upload_to='backups/')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True,default=None)
    file_size = models.PositiveIntegerField()
    is_automated = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Backup {self.created_at}"
    
# administration/models.py
class SystemSetting(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.JSONField()
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.key

class HealthMetric(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    cpu_usage = models.FloatField()  # percentage
    memory_usage = models.FloatField()  # percentage
    disk_usage = models.FloatField()  # percentage
    disk_space = models.FloatField()  # in GB
    response_time = models.FloatField()  # in ms
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
        ]
    
    def __str__(self):
        return f"Metrics at {self.timestamp}"
    
# administration/models.py
class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('read', 'Read'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model = models.CharField(max_length=100, blank=True)  # Model name if applicable
    object_id = models.CharField(max_length=100, blank=True)  # ID of affected object
    details = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['action', '-timestamp']),
            models.Index(fields=['model', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user} {self.get_action_display()} at {self.timestamp}"

class Notification(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    related_model = models.CharField(max_length=50, blank=True, null=True)
    related_id = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read', '-created_at']),
        ]

    def __str__(self):
        return f"Notification for {self.user_id}: {self.message}"


class RumMetric(models.Model):
    """One real-user-monitoring sample reported by the browser."""

    name = models.CharField(max_length=32)
    value = models.FloatField()
    rating = models.CharField(max_length=16, blank=True)
    page_path = models.CharField(max_length=200)
    device = models.CharField(max_length=16, blank=True)
    connection = models.CharField(max_length=16, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name', '-created_at']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f'{self.name}={self.value} on {self.page_path}'


class BackgroundJob(models.Model):
    """Database-backed background job processed by ``manage.py run_worker``."""

    STATUS_CHOICES = [
        ('queued', 'Queued'),
        ('running', 'Running'),
        ('succeeded', 'Succeeded'),
        ('failed', 'Failed'),
    ]

    job_type = models.CharField(max_length=64)
    payload = models.JSONField(default=dict, blank=True)
    status = models.CharField(
        max_length=16, choices=STATUS_CHOICES, default='queued')
    result = models.JSONField(default=dict, blank=True)
    error = models.TextField(blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='background_jobs')
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f'{self.job_type} [{self.status}]'
