from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from administration.models import User, Role
from workflow.models import (
    ProductionLine, ProductionOrder, Product, Workflow, Stage,
)


def make_user(role_name='production_manager'):
    role, _ = Role.objects.get_or_create(name=role_name)
    return User.objects.create_user(
        email=f'{role_name}@example.com',
        full_name='Test User',
        password='secret1234',
        role=role,
    )


def make_line(name='Line A'):
    return ProductionLine.objects.create(
        line_name=name,
        capacity_limit=10,
        oee_target=90,
        status='Active',
        maintenance_schedule='None',
        preferred_shift='Day',
    )


def make_order(line, name, status, days_ago=10, duration_days=1):
    product, _ = Product.objects.get_or_create(
        name='Widget', defaults={'specifications': ''})
    start = timezone.now() - timedelta(days=days_ago)
    return ProductionOrder.objects.create(
        order_name=name,
        priority='High',
        product=product,
        quantity=5,
        start_date=start,
        end_date=start + timedelta(days=duration_days),
        production_line=line,
        status=status,
    )


class ProductionPerformanceReportTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=make_user())

    def test_line_without_orders_does_not_divide_by_zero(self):
        make_line('Empty Line')
        response = self.client.get(
            '/api/reports/production/performance/')
        self.assertEqual(response.status_code, 200, response.content)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['total_orders'], 0)
        self.assertEqual(float(data[0]['completion_rate']), 0)

    def test_completion_rate_and_delayed_orders(self):
        line = make_line()
        make_order(line, 'done', 'Completed', days_ago=20)
        make_order(line, 'pending-overdue', 'Pending', days_ago=5)
        make_order(line, 'in-progress-fresh', 'In Progress', days_ago=0)

        response = self.client.get(
            '/api/reports/production/performance/')
        self.assertEqual(response.status_code, 200, response.content)
        data = response.json()[0]
        self.assertEqual(data['total_orders'], 3)
        self.assertEqual(data['completed_orders'], 1)
        self.assertEqual(float(data['completion_rate']), 33.33)
        # only the overdue order that is not Completed counts as delayed
        self.assertEqual(data['delayed_orders'], 1)
        self.assertIsNotNone(data['average_duration'])


class OtherReportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=make_user())
        self.line = make_line()
        product, _ = Product.objects.get_or_create(
            name='Widget', defaults={'specifications': ''})
        self.workflow = Workflow.objects.create(
            name='WF', description='flow', product=product)
        Stage.objects.create(
            name='Cut',
            description='cutting',
            duration=30,
            workflow=self.workflow,
        )
        Stage.objects.create(
            name='Weld',
            description='welding',
            duration=60,
            workflow=self.workflow,
        )

    def test_order_status_report(self):
        make_order(self.line, 'a', 'Completed')
        make_order(self.line, 'b', 'Pending')
        response = self.client.get('/api/reports/orders/status/')
        self.assertEqual(response.status_code, 200, response.content)
        data = {row['status']: row for row in response.json()}
        self.assertEqual(data['Completed']['count'], 1)
        self.assertEqual(data['Pending']['total_quantity'], 5)

    def test_workflow_analysis_report(self):
        response = self.client.get('/api/reports/workflow/analysis/')
        self.assertEqual(response.status_code, 200, response.content)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['total_stages'], 2)
        self.assertEqual(data[0]['avg_stage_duration'], 45)
        self.assertEqual(data[0]['longest_stage']['name'], 'Weld')

    def test_stage_duration_report(self):
        response = self.client.get('/api/reports/stages/durations/')
        self.assertEqual(response.status_code, 200, response.content)
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['workflow_name'], 'WF')

    def test_export_csv_and_excel(self):
        make_order(self.line, 'a', 'Completed')
        response = self.client.get('/api/reports/export/production/csv/')
        self.assertEqual(response.status_code, 200, response.content)
        response = self.client.get('/api/reports/export/production/excel/')
        self.assertEqual(response.status_code, 200, response.content)
