from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from administration.models import User, Role
from workflow.models import ProductionLine, ProductionOrder, Product
from workcentre.models import WorkCenter
from .models import WorkInstruction, WorkOrder, JobCard


def make_user(role_name='production_manager'):
    role, _ = Role.objects.get_or_create(name=role_name)
    return User.objects.create_user(
        email=f'{role_name}@example.com',
        full_name='Test User',
        password='secret1234',
        role=role,
    )


class GenerateJobCardsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=make_user())
        self.center = WorkCenter.objects.create(
            name='Center A', code='CA-1', location='B1')
        self.line = ProductionLine.objects.create(
            line_name='Line A',
            capacity_limit=10,
            oee_target=90,
            status='Active',
            maintenance_schedule='None',
            preferred_shift='Day',
        )
        self.line.work_centers.add(self.center)
        self.instruction = WorkInstruction.objects.create(
            title='WI',
            task_steps='  Step one  \n\nStep two\n',
            tools_required='tools',
            materials_required='materials',
            step_description='desc',
            status='Not Started',
        )
        self.order = WorkOrder.objects.create(
            name='WO-1',
            quantity_required=5,
            due_date=timezone.now(),
            priority='Low',
            work_instruction=self.instruction,
            production_line=self.line,
        )

    def test_generate_job_cards_creates_cards(self):
        response = self.client.post(
            f'/api/work_orders/{self.order.pk}/generate_job_cards/')
        self.assertEqual(response.status_code, 200, response.content)
        body = response.json()
        self.assertEqual(body['created'], 2)
        self.assertEqual(body['total'], 2)
        card = JobCard.objects.get(task_name='Step one')
        self.assertEqual(card.assigned_to, self.center)
        self.assertEqual(card.status, 'Not Started')

    def test_generate_job_cards_is_idempotent(self):
        self.client.post(
            f'/api/work_orders/{self.order.pk}/generate_job_cards/')
        response = self.client.post(
            f'/api/work_orders/{self.order.pk}/generate_job_cards/')
        self.assertEqual(response.status_code, 200, response.content)
        body = response.json()
        self.assertEqual(body['created'], 0)
        self.assertEqual(body['total'], 2)
        self.assertEqual(JobCard.objects.count(), 2)

    def test_create_work_order_generates_job_cards(self):
        response = self.client.post('/api/work_orders/', {
            'name': 'WO-2',
            'quantity_required': 3,
            'due_date': timezone.now().isoformat(),
            'priority': 'Medium',
            'work_instruction': self.instruction.pk,
            'production_line': self.line.pk,
        }, format='json')
        self.assertEqual(response.status_code, 201, response.content)
        order = WorkOrder.objects.get(pk=response.json()['id'])
        self.assertEqual(order.job_cards.count(), 2)

    def test_job_cards_filter_by_work_order(self):
        self.client.post(
            f'/api/work_orders/{self.order.pk}/generate_job_cards/')
        response = self.client.get(
            f'/api/job_cards/?work_order_id={self.order.pk}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def _make_production_order(self, name='PO-1'):
        product = Product.objects.create(
            name=f'Product-{name}', specifications='')
        return ProductionOrder.objects.create(
            order_name=name,
            priority='High',
            product=product,
            quantity=5,
            start_date=timezone.now(),
            end_date=timezone.now(),
            production_line=self.line,
        )

    def test_create_work_order_with_production_order_link(self):
        po = self._make_production_order()
        response = self.client.post('/api/work_orders/', {
            'name': 'WO-linked',
            'quantity_required': 2,
            'due_date': timezone.now().isoformat(),
            'priority': 'Medium',
            'work_instruction': self.instruction.pk,
            'production_line': self.line.pk,
            'production_order': po.pk,
        }, format='json')
        self.assertEqual(response.status_code, 201, response.content)
        self.assertEqual(response.json()['production_order'], po.pk)
        order = WorkOrder.objects.get(pk=response.json()['id'])
        self.assertEqual(order.production_order, po)

    def test_work_orders_filter_by_production_order(self):
        po = self._make_production_order()
        self.order.production_order = po
        self.order.save(update_fields=['production_order'])

        response = self.client.get(
            f'/api/work_orders/?production_order={po.pk}')
        self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['id'], self.order.pk)

    def test_production_order_exposes_linked_work_orders(self):
        po = self._make_production_order()
        self.order.production_order = po
        self.order.save(update_fields=['production_order'])

        response = self.client.get(f'/api/production-orders/{po.pk}/')
        self.assertEqual(response.status_code, 200, response.content)
        data = response.json()
        self.assertEqual(data['work_orders'], [self.order.pk])
        self.assertEqual(data['work_orders_count'], 1)

    def test_create_work_order_requires_authentication(self):
        anonymous = APIClient()
        response = anonymous.post('/api/work_orders/', {
            'name': 'WO-anon',
            'quantity_required': 1,
            'due_date': timezone.now().isoformat(),
            'priority': 'Low',
            'work_instruction': self.instruction.pk,
        }, format='json')
        self.assertEqual(response.status_code, 401)
