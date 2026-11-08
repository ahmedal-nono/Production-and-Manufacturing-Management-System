from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from administration.models import User, Role
from workflow.models import ProductionLine
from work_instructions.models import WorkInstruction, WorkOrder, JobCard
from .models import Inspection, InspectionChecklist, ReworkRequest


def make_user(role_name='quality_control_manager'):
    role, _ = Role.objects.get_or_create(name=role_name)
    return User.objects.create_user(
        email=f'{role_name}@example.com',
        full_name='Test User',
        password='secret1234',
        role=role,
    )


def make_work_order(line=None, steps='Step one\nStep two\n'):
    instruction = WorkInstruction.objects.create(
        title='WI',
        task_steps=steps,
        tools_required='tools',
        materials_required='materials',
        step_description='desc',
        status='Not Started',
    )
    order = WorkOrder.objects.create(
        name='WO-1',
        quantity_required=10,
        due_date=timezone.now(),
        priority='High',
        work_instruction=instruction,
        production_line=line,
    )
    JobCard.objects.create(
        work_order=order,
        task_name='Step one',
        required_tools='tools',
        required_materials='materials',
        status='Not Started',
    )
    JobCard.objects.create(
        work_order=order,
        task_name='Step two',
        required_tools='tools',
        required_materials='materials',
        status='Not Started',
    )
    return order


class QualityControlApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=make_user())
        self.line = ProductionLine.objects.create(
            line_name='Line A',
            capacity_limit=10,
            oee_target=90,
            status='Active',
            maintenance_schedule='None',
            preferred_shift='Day',
        )
        self.order = make_work_order(self.line)

    def test_workorders_list_returns_work_order_fields(self):
        response = self.client.get('/api/workorders/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'WO-1')
        self.assertEqual(data[0]['quantity_required'], 10)
        self.assertEqual(data[0]['production_line_name'], 'Line A')
        self.assertIsNone(data[0]['latest_decision'])

    def test_workorder_detail_includes_job_cards(self):
        response = self.client.get(f'/api/workorders/{self.order.pk}/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['job_cards']), 2)
        self.assertEqual(data['job_cards'][0]['task_name'], 'Step one')

    def test_create_inspection_builds_checklist_from_job_cards(self):
        response = self.client.post('/api/inspections/', {
            'work_order': self.order.pk,
            'defect_type': 'Crack',
            'severity': 'major',
            'affected_component': 'Arm',
            'description': 'visible crack',
            'final_decision': 'approve',
        }, format='json')
        self.assertEqual(response.status_code, 201, response.content)
        inspection = Inspection.objects.get(pk=response.json()['id'])
        self.assertEqual(inspection.checklist_items.count(), 2)
        self.assertEqual(
            list(inspection.checklist_items.values_list(
                'job_card__task_name', flat=True)),
            ['Step one', 'Step two'],
        )

    def test_create_inspection_without_defect_fields(self):
        response = self.client.post('/api/inspections/', {
            'work_order': self.order.pk,
            'final_decision': 'approve',
        }, format='json')
        self.assertEqual(response.status_code, 201, response.content)
        inspection = Inspection.objects.get(pk=response.json()['id'])
        self.assertEqual(inspection.defect_type, '')

    def test_rework_decision_creates_rework_request_once(self):
        inspection = Inspection.objects.create(
            work_order=self.order,
            final_decision='approve',
        )
        response = self.client.patch(
            f'/api/inspections/{inspection.pk}/',
            {'final_decision': 'rework'},
            format='json',
        )
        self.assertEqual(response.status_code, 200, response.content)
        response = self.client.patch(
            f'/api/inspections/{inspection.pk}/',
            {'final_decision': 'rework'},
            format='json',
        )
        self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual(ReworkRequest.objects.count(), 1)

    def test_create_inspection_with_rework_decision_creates_rework_request(self):
        response = self.client.post('/api/inspections/', {
            'work_order': self.order.pk,
            'final_decision': 'rework',
        }, format='json')
        self.assertEqual(response.status_code, 201, response.content)
        inspection_id = response.json()['id']
        self.assertEqual(ReworkRequest.objects.count(), 1)
        rework = ReworkRequest.objects.get()
        self.assertEqual(rework.inspection.pk, inspection_id)
        self.assertEqual(rework.status, 'pending')

    def test_rework_list_exposes_inspection_fields(self):
        inspection = Inspection.objects.create(
            work_order=self.order,
            defect_type='Crack',
            severity='critical',
            affected_component='Arm',
            description='crack found',
            final_decision='rework',
        )
        ReworkRequest.objects.create(inspection=inspection, status='pending')
        response = self.client.get('/api/rework-requests/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['product_name'], 'WO-1')
        self.assertEqual(data[0]['workorder_id'], self.order.pk)
        self.assertEqual(data[0]['defect_type'], 'Crack')
        self.assertEqual(data[0]['status'], 'pending')

    def test_rework_status_update(self):
        inspection = Inspection.objects.create(
            work_order=self.order, final_decision='rework')
        rework = ReworkRequest.objects.create(
            inspection=inspection, status='pending')
        response = self.client.patch(
            f'/api/rework-requests/{rework.pk}/',
            {'status': 'approved'},
            format='json',
        )
        self.assertEqual(response.status_code, 200, response.content)
        rework.refresh_from_db()
        self.assertEqual(rework.status, 'approved')

    def test_checklist_partial_update(self):
        inspection = Inspection.objects.create(
            work_order=self.order, final_decision='approve')
        item = InspectionChecklist.objects.create(
            inspection=inspection,
            job_card=JobCard.objects.first(),
        )
        response = self.client.patch(
            f'/api/checklist/{item.pk}/',
            {'state': 'pass', 'note': 'looks good'},
            format='json',
        )
        self.assertEqual(response.status_code, 200, response.content)
        item.refresh_from_db()
        self.assertEqual(item.state, 'pass')
        self.assertEqual(item.note, 'looks good')
