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
