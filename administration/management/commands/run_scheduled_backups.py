# administration/management/commands/run_scheduled_backups.py
from django.core.management.base import BaseCommand
from django.conf import settings
from administration.models import BackupConfig, BackupRecord
from django.contrib.auth import get_user_model
import os
from datetime import datetime, time, timedelta
import subprocess

class Command(BaseCommand):
    help = 'Run scheduled database backups'
    
    def handle(self, *args, **options):
        now = datetime.now()
        current_time = now.time()
        
        # Find active backup configurations that match current schedule
        for config in BackupConfig.objects.filter(is_active=True):
            # Check if it's time to run
            if (
                (config.schedule_type == 'daily') or
                (config.schedule_type == 'weekly' and now.weekday() == 0) or  # Monday
                (config.schedule_type == 'monthly' and now.day == 1)
            ):
                if (current_time.hour == config.schedule_time.hour and 
                    current_time.minute == config.schedule_time.minute):
                    
                    self.run_backup(config)
    
    def run_backup(self, config):
        admin_user = get_user_model().objects.filter(is_superuser=True).first()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"fpms_auto_backup_{timestamp}.sql"
        backup_path = os.path.join(settings.MEDIA_ROOT, 'backups', filename)
        
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        
        db_settings = settings.DATABASES['default']
        command = [
            'mysqldump',
            '-u', db_settings['USER'],
            '-p' + db_settings['PASSWORD'],
            '-h', db_settings['HOST'],
            db_settings['NAME'],
            '--result-file=' + backup_path
        ]
        
        try:
            subprocess.run(command, check=True)
            file_size = os.path.getsize(backup_path)
            
            BackupRecord.objects.create(
                backup_file=f'backups/{filename}',
                created_by=admin_user,
                file_size=file_size,
                is_automated=True
            )
            
            # Update last run time
            config.last_run = datetime.now()
            config.save()
            
            # Clean up old backups
            self.cleanup_old_backups(config.retain_days)
        except subprocess.CalledProcessError as e:
            # Log error
            pass
    
    def cleanup_old_backups(self, retain_days):
        cutoff = datetime.now() - timedelta(days=retain_days)
        old_backups = BackupRecord.objects.filter(
            created_at__lt=cutoff,
            is_automated=True
        )
        
        for backup in old_backups:
            try:
                os.remove(backup.backup_file.path)
                backup.delete()
            except:
                # Log error
                pass