from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Department, Role, Notification, ActivityLog


class UserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        admin_role = Role.objects.create(name='admin')
        self.admin = User.objects.create_user(
            email='admin@example.com',
            full_name='Admin User',
            password='secret1234',
            role=admin_role,
        )
        self.editable = User.objects.create_user(
            email='user@example.com',
            full_name='Regular User',
            password='secret1234',
        )
        self.client.force_authenticate(user=self.admin)

    def test_user_list_returns_users(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)
        emails = sorted(u['email'] for u in response.json())
        self.assertEqual(emails, ['admin@example.com', 'user@example.com'])

    def test_login_success(self):
        response = self.client.post(
            '/users/login/',
            {'email': 'admin@example.com', 'password': 'secret1234'},
            format='json',
        )
        self.assertEqual(response.status_code, 200, response.content)
        body = response.json()
        self.assertEqual(body['user']['email'], 'admin@example.com')
        self.assertIn('access', body)
        self.assertIn('refresh', body)

    def test_login_failure_returns_401(self):
        response = self.client.post(
            '/users/login/',
            {'email': 'admin@example.com', 'password': 'wrong'},
            format='json',
        )
        self.assertEqual(response.status_code, 401)

    def test_user_endpoints_require_authentication(self):
        anonymous = APIClient()
        self.assertEqual(anonymous.get('/users/').status_code, 401)
        self.assertEqual(anonymous.get('/api/admin/roles/').status_code, 401)
        self.assertEqual(anonymous.get('/api/admin/activity-logs/').status_code, 401)

    def test_user_endpoints_forbidden_for_non_admin(self):
        self.client.force_authenticate(user=self.editable)
        self.assertEqual(self.client.get('/users/').status_code, 403)
        self.assertEqual(self.client.get('/api/admin/departments/').status_code, 403)

    def test_create_user_with_department_and_role(self):
        response = self.client.post('/users/', {
            'full_name': 'New Person',
            'email': 'new@example.com',
            'password': 'secret1234',
            'department': 'Quality',
            'role': 'operator',
        }, format='json')
        self.assertEqual(response.status_code, 201, response.content)
        user = User.objects.get(email='new@example.com')
        self.assertEqual(user.department.name, 'Quality')
        self.assertEqual(user.role.name, 'operator')
        self.assertEqual(response.json()['role'], 'Operator')

    def test_patch_user_without_department_or_role(self):
        response = self.client.patch(
            f'/users/{self.editable.pk}/',
            {'full_name': 'Renamed'},
            format='json',
        )
        self.assertEqual(response.status_code, 200, response.content)
        self.editable.refresh_from_db()
        self.assertEqual(self.editable.full_name, 'Renamed')

    def test_user_role_round_trips(self):
        role = Role.objects.create(name='production_manager')
        department = Department.objects.create(name='Production')
        user = User.objects.create_user(
            email='pm@example.com',
            full_name='PM',
            password='secret1234',
            role=role,
            department=department,
        )
        response = self.client.get(f'/users/{user.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['role'], 'Production Manager')
        self.assertEqual(response.json()['department'], 'Production')

        # PATCH with the role key (as sent by the create/edit select options)
        response = self.client.patch(f'/users/{user.pk}/', {
            'full_name': 'PM2',
            'department': 'Production',
            'role': 'production_manager',
        }, format='json')
        self.assertEqual(response.status_code, 200, response.content)

        # PATCH with the display label (as returned by GET /users/)
        response = self.client.patch(f'/users/{user.pk}/', {
            'full_name': 'PM3',
            'department': 'Production',
            'role': 'Production Manager',
        }, format='json')
        self.assertEqual(response.status_code, 200, response.content)
        user.refresh_from_db()
        self.assertEqual(user.role.name, 'production_manager')
        self.assertEqual(user.full_name, 'PM3')


class NotificationApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='someone@example.com',
            full_name='Someone',
            password='secret1234',
        )
        self.client.force_authenticate(user=self.user)

    def test_create_list_and_filter(self):
        response = self.client.post('/notifications/', {
            'user': self.user.pk,
            'message': 'Order completed',
            'url': '/orders/1/',
            'related_model': 'ProductionOrder',
            'related_id': 1,
        }, format='json')
        self.assertEqual(response.status_code, 201, response.content)

        response = self.client.get('/notifications/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

        response = self.client.get(
            f'/notifications/?user={self.user.pk}')
        self.assertEqual(len(response.json()), 1)

        other = User.objects.create_user(
            email='other@example.com',
            full_name='Other',
            password='secret1234',
        )
        response = self.client.get(f'/notifications/?user={other.pk}')
        self.assertEqual(len(response.json()), 0)

    def test_mark_as_read(self):
        notification = Notification.objects.create(
            user=self.user, message='hello')
        response = self.client.patch(
            f'/notifications/{notification.pk}/',
            {'is_read': True},
            format='json',
        )
        self.assertEqual(response.status_code, 200, response.content)
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)


class ActivityLogActorTests(TestCase):
    """Verify ActivityLog records the real actor of a change."""

    def setUp(self):
        self.client = APIClient()
        admin_role = Role.objects.create(name='admin')
        self.admin = User.objects.create_user(
            email='auditor@example.com',
            full_name='Auditor',
            password='secret1234',
            role=admin_role,
        )
        self.access = str(RefreshToken.for_user(self.admin).access_token)

    def _auth_headers(self, **extra):
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access}'}
        headers.update(extra)
        return headers

    def test_model_create_is_attributed_to_jwt_actor(self):
        response = self.client.post(
            '/api/admin/departments/',
            {'name': 'Logging', 'description': ''},
            format='json',
            **self._auth_headers(),
        )
        self.assertEqual(response.status_code, 201, response.content)
        department_id = response.json()['id']

        entry = ActivityLog.objects.filter(
            model='Department', object_id=str(department_id)).first()
        self.assertIsNotNone(entry)
        self.assertEqual(entry.action, 'create')
        self.assertEqual(entry.user_id, self.admin.pk)
        self.assertEqual(entry.ip_address, '127.0.0.1')
        self.assertEqual(entry.details.get('request_method'), 'POST')
        self.assertIn('departments', entry.details.get('request_path', ''))

    def test_model_update_is_attributed_to_jwt_actor(self):
        department = Department.objects.create(name='Original')
        response = self.client.patch(
            f'/api/admin/departments/{department.pk}/',
            {'name': 'Renamed'},
            format='json',
            **self._auth_headers(),
        )
        self.assertEqual(response.status_code, 200, response.content)

        entry = ActivityLog.objects.filter(
            model='Department', object_id=str(department.pk),
            action='update').first()
        self.assertIsNotNone(entry)
        self.assertEqual(entry.user_id, self.admin.pk)

    def test_login_is_logged_for_the_logging_in_user(self):
        self.client.post(
            '/users/login/',
            {'email': self.admin.email, 'password': 'secret1234'},
            format='json',
        )
        entry = ActivityLog.objects.filter(action='login').first()
        self.assertIsNotNone(entry)
        self.assertEqual(entry.user_id, self.admin.pk)
        self.assertEqual(entry.details.get('email'), self.admin.email)

    def test_change_without_request_has_no_actor(self):
        department = Department.objects.create(name='No request')
        entry = ActivityLog.objects.filter(
            model='Department', object_id=str(department.pk)).first()
        self.assertIsNotNone(entry)
        self.assertIsNone(entry.user_id)
        self.assertIsNone(entry.ip_address)

    def test_x_forwarded_for_is_used_for_client_ip(self):
        response = self.client.post(
            '/api/admin/departments/',
            {'name': 'Proxy', 'description': ''},
            format='json',
            **self._auth_headers(
                HTTP_X_FORWARDED_FOR='203.0.113.9, 10.0.0.1'),
        )
        self.assertEqual(response.status_code, 201, response.content)
        department_id = response.json()['id']
        entry = ActivityLog.objects.filter(
            model='Department', object_id=str(department_id)).first()
        self.assertEqual(entry.ip_address, '203.0.113.9')

    def test_system_apps_are_not_logged(self):
        # A session-style bookkeeping save must not create audit noise.
        from django.contrib.contenttypes.models import ContentType
        ContentType.objects.get_or_create(
            app_label='administration', model='activitylogprobe')
        self.assertFalse(
            ActivityLog.objects.filter(model='ContentType').exists())

import tempfile
from datetime import timedelta

from django.test import override_settings
from django.utils import timezone

from .models import BackgroundJob, BackupRecord, RumMetric
from .jobs import enqueue, prune, recover_stale, register, run_pending


@register('test.flaky')
def _flaky_handler(job):
    """Fails ``fail_times`` attempts, then succeeds (used by the tests)."""
    if job.attempts <= job.payload.get('fail_times', 0):
        raise RuntimeError('temporary failure')
    return {'attempts': job.attempts}


class RumMetricApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_anonymous_can_post_bulk_metrics(self):
        response = self.client.post(
            '/api/admin/rum/',
            {
                'metrics': [
                    {'name': 'LCP', 'value': 1234.5, 'rating': 'good',
                     'page_path': '/production', 'device': 'desktop',
                     'connection': '4g'},
                    {'name': 'CLS', 'value': 0.05, 'rating': 'good',
                     'page_path': '/production', 'device': 'desktop',
                     'connection': '4g'},
                ]
            },
            format='json',
        )
        self.assertEqual(response.status_code, 201, response.content)
        self.assertEqual(response.json()['received'], 2)
        self.assertEqual(RumMetric.objects.count(), 2)

    def test_invalid_metric_name_is_rejected(self):
        response = self.client.post(
            '/api/admin/rum/',
            {'name': 'NOPE', 'value': 1, 'page_path': '/'},
            format='json',
        )
        self.assertEqual(response.status_code, 400)

    def test_listing_requires_admin(self):
        self.assertEqual(self.client.get('/api/admin/rum/').status_code, 401)

    def test_summary_requires_admin(self):
        self.assertEqual(
            self.client.get('/api/admin/rum/summary/').status_code, 401)

    def test_summary_reports_percentiles_and_pages(self):
        admin_role = Role.objects.create(name='admin')
        admin = User.objects.create_user(
            email='rum-admin@example.com',
            full_name='RUM Admin',
            password='secret1234',
            role=admin_role,
        )
        self.client.force_authenticate(user=admin)

        for value in (1000, 2000, 3000, 4000):
            RumMetric.objects.create(
                name='LCP', value=value, rating='good',
                page_path='/production', device='desktop',
                connection='4g')
        RumMetric.objects.create(
            name='CLS', value=0.05, rating='good',
            page_path='/production', device='desktop', connection='4g')

        response = self.client.get('/api/admin/rum/summary/?days=7')
        self.assertEqual(response.status_code, 200, response.content)
        data = response.json()
        self.assertEqual(data['sample_count'], 5)
        self.assertEqual(data['window_days'], 7)

        metrics = {row['name']: row for row in data['metrics']}
        self.assertEqual(metrics['LCP']['p75'], 3000)
        self.assertEqual(metrics['LCP']['p95'], 4000)
        self.assertEqual(metrics['LCP']['ratings']['good'], 2)
        self.assertEqual(metrics['LCP']['ratings']['needs_improvement'], 2)
        self.assertEqual(metrics['LCP']['ratings']['poor'], 0)
        self.assertEqual(metrics['CLS']['count'], 1)

        self.assertEqual(len(data['pages']), 1)
        self.assertEqual(data['pages'][0]['page_path'], '/production')
        self.assertEqual(data['pages'][0]['count'], 5)
        self.assertEqual(data['pages'][0]['lcp_p75'], 3000)
        # No INP samples on that page: report null so the UI shows a dash.
        self.assertIsNone(data['pages'][0]['inp_p75'])


class BackgroundJobTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        admin_role = Role.objects.create(name='admin')
        self.admin = User.objects.create_user(
            email='jobs-admin@example.com',
            full_name='Jobs Admin',
            password='secret1234',
            role=admin_role,
        )
        self.client.force_authenticate(user=self.admin)

    def test_enqueue_and_run_echo_job(self):
        job = enqueue('system.echo', {'hello': 'world'}, user=self.admin)
        self.assertEqual(job.status, 'queued')
        self.assertEqual(run_pending(limit=1), 1)
        job.refresh_from_db()
        self.assertEqual(job.status, 'succeeded', job.error)
        self.assertEqual(job.result, {'echo': {'hello': 'world'}})
        self.assertIsNotNone(job.started_at)
        self.assertIsNotNone(job.finished_at)

    def test_failing_handler_marks_job_failed(self):
        job = enqueue('missing.handler', max_attempts=1)
        run_pending(limit=1)
        job.refresh_from_db()
        self.assertEqual(job.status, 'failed')
        self.assertIn('No handler', job.error)

    def test_failed_job_is_retried_with_backoff(self):
        job = enqueue('test.flaky', {'fail_times': 1}, max_attempts=3)
        run_pending(limit=1)
        job.refresh_from_db()
        self.assertEqual(job.status, 'queued')
        self.assertEqual(job.attempts, 1)
        self.assertIn('temporary failure', job.error)
        self.assertGreater(job.available_at, timezone.now())

        BackgroundJob.objects.filter(pk=job.pk).update(
            available_at=timezone.now())
        run_pending(limit=1)
        job.refresh_from_db()
        self.assertEqual(job.status, 'succeeded', job.error)
        self.assertEqual(job.attempts, 2)
        self.assertEqual(job.result, {'attempts': 2})

    def test_job_fails_after_max_attempts(self):
        job = enqueue('test.flaky', {'fail_times': 99}, max_attempts=2)
        for _ in range(2):
            BackgroundJob.objects.filter(pk=job.pk).update(
                available_at=timezone.now())
            run_pending(limit=1)
        job.refresh_from_db()
        self.assertEqual(job.status, 'failed')
        self.assertEqual(job.attempts, 2)
        self.assertIn('temporary failure', job.error)

    def test_job_scheduled_in_the_future_is_not_run(self):
        job = enqueue('system.echo', delay=60)
        self.assertEqual(run_pending(limit=1), 0)
        job.refresh_from_db()
        self.assertEqual(job.status, 'queued')

    def test_recover_stale_requeues_orphaned_job(self):
        job = enqueue('system.echo', max_attempts=3)
        BackgroundJob.objects.filter(pk=job.pk).update(
            status='running', attempts=1,
            started_at=timezone.now() - timedelta(seconds=1200))
        report = recover_stale(age_seconds=600)
        self.assertEqual(report, {'requeued': 1, 'failed': 0})
        job.refresh_from_db()
        self.assertEqual(job.status, 'queued')
        self.assertIn('Worker stopped', job.error)

    def test_recover_stale_fails_exhausted_job(self):
        job = enqueue('system.echo', max_attempts=1)
        BackgroundJob.objects.filter(pk=job.pk).update(
            status='running', attempts=1,
            started_at=timezone.now() - timedelta(seconds=1200))
        report = recover_stale(age_seconds=600)
        self.assertEqual(report, {'requeued': 0, 'failed': 1})
        job.refresh_from_db()
        self.assertEqual(job.status, 'failed')

    def test_prune_deletes_only_old_finished_jobs(self):
        old = enqueue('system.echo')
        BackgroundJob.objects.filter(pk=old.pk).update(
            status='succeeded',
            created_at=timezone.now() - timedelta(days=40))
        fresh = enqueue('system.echo')
        self.assertEqual(prune(days=30), 1)
        self.assertFalse(BackgroundJob.objects.filter(pk=old.pk).exists())
        self.assertTrue(BackgroundJob.objects.filter(pk=fresh.pk).exists())

    def test_enqueue_backup_endpoint_returns_queued_job(self):
        response = self.client.post(
            '/api/admin/backups/enqueue_backup/', {}, format='json')
        self.assertEqual(response.status_code, 202, response.content)
        body = response.json()
        self.assertEqual(body['status'], 'queued')
        self.assertTrue(BackgroundJob.objects.filter(pk=body['id']).exists())

    def test_backup_job_creates_record(self):
        media_root = tempfile.mkdtemp()
        with override_settings(MEDIA_ROOT=media_root):
            job = enqueue(
                'backup.create', {'created_by_id': self.admin.id},
                user=self.admin)
            run_pending(limit=1)
            job.refresh_from_db()
            self.assertEqual(job.status, 'succeeded', job.error)
            record = BackupRecord.objects.get(pk=job.result['backup_id'])
            self.assertGreater(record.file_size, 0)
            self.assertTrue(record.backup_file.storage.exists(record.backup_file.name))
