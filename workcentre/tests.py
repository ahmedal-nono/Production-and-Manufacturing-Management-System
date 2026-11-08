from django.test import TestCase
from rest_framework.test import APIClient

from administration.models import User, Role
from .models import WorkCenter, Workstation, Maintenance


def make_user(role_name='production_manager'):
    role, _ = Role.objects.get_or_create(name=role_name)
    return User.objects.create_user(
        email=f'{role_name}@example.com',
        full_name='Test User',
        password='secret1234',
        role=role,
    )


class WorkstationApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=make_user())
        self.center = WorkCenter.objects.create(
            name='Center A', code='CA-1', location='B1')
        self.station = Workstation.objects.create(
            name='Station 1',
            status='Active',
            capacity=3,
            description='desc',
            work_center=self.center,
            machines=['M1'],
            tools=['T1'],
        )

    def test_list_workstations(self):
        response = self.client.get('/api/workcentre/workstations/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['work_center'], self.center.pk)

    def test_create_without_work_center(self):
        response = self.client.post('/api/workcentre/workstations/', {
            'name': 'Station 2',
            'status': 'Active',
            'capacity': 1,
            'description': '',
            'machines': [],
            'tools': [],
            'work_center': '',
        }, format='json')
        self.assertEqual(response.status_code, 201, response.content)
        station = Workstation.objects.get(name='Station 2')
        self.assertIsNone(station.work_center)

    def test_create_with_work_center(self):
        response = self.client.post('/api/workcentre/workstations/', {
            'name': 'Station 3',
            'status': 'Active',
            'capacity': 1,
            'description': '',
            'machines': [],
            'tools': [],
            'work_center': self.center.pk,
        }, format='json')
        self.assertEqual(response.status_code, 201, response.content)

    def test_full_update(self):
        response = self.client.put(
            f'/api/workcentre/workstations/{self.station.pk}/',
            {
                'name': 'Station 1 renamed',
                'status': 'Inactive',
                'capacity': 5,
                'description': 'new',
                'machines': ['M1', 'M2'],
                'tools': ['T1'],
                'work_center': self.center.pk,
            },
            format='json',
        )
        self.assertEqual(response.status_code, 200, response.content)
        self.station.refresh_from_db()
        self.assertEqual(self.station.name, 'Station 1 renamed')
        self.assertEqual(self.station.status, 'Inactive')

    def test_partial_update(self):
        response = self.client.patch(
            f'/api/workcentre/workstations/{self.station.pk}/',
            {'capacity': 9},
            format='json',
        )
        self.assertEqual(response.status_code, 200, response.content)
        self.station.refresh_from_db()
        self.assertEqual(self.station.capacity, 9)

    def test_delete(self):
        response = self.client.delete(
            f'/api/workcentre/workstations/{self.station.pk}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Workstation.objects.count(), 0)

    def test_custom_action(self):
        response = self.client.get(
            f'/api/workcentre/workstations/{self.station.pk}/custom_action/')
        self.assertEqual(response.status_code, 200, response.content)

    def test_custom_action_missing_station(self):
        response = self.client.get(
            '/api/workcentre/workstations/999999/custom_action/')
        self.assertEqual(response.status_code, 404)

    def test_maintenance_crud(self):
        response = self.client.post('/api/workcentre/maintenances/', {
            'workstation': self.station.pk,
            'maintenance_date': '2026-01-15',
            'maintenance_time': '10:00:00',
            'recurrence': 'Monthly',
            'description': 'lubricate',
            'assigned_staff': [],
        }, format='json')
        self.assertEqual(response.status_code, 201, response.content)
        self.assertEqual(Maintenance.objects.count(), 1)

    def test_requires_authentication(self):
        anonymous = APIClient()
        self.assertEqual(anonymous.get('/api/workcentre/workcenters/').status_code, 401)

    def test_operator_cannot_write(self):
        self.client.force_authenticate(user=make_user('operator'))
        response = self.client.post('/api/workcentre/workcenters/', {
            'name': 'Nope', 'code': 'NOPE-1', 'location': 'X',
        }, format='json')
        self.assertEqual(response.status_code, 403)
