from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Avg, Sum, F, Min, Max, Q
from django.db.models.functions import Cast
from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.utils.dateparse import parse_duration
from django.http import HttpResponse
from io import BytesIO
import pandas as pd

from administration.permissions import RoleWritePermission
from .models import Issue, Report, ReportTemplate, ScheduledReport
from .serializers import (
    IssueListSerializer, IssueDetailSerializer,
    ReportListSerializer, ReportDetailSerializer,
    ReportTemplateSerializer, ScheduledReportSerializer,
    ProductionPerformanceReportSerializer,
    WorkflowAnalysisReportSerializer,
    ProductionOrderStatusSerializer,
    StageDurationSerializer
)
from workflow.models import ProductionOrder, ProductionLine, Workflow, Stage

REPORTS_ROLES = (
    'admin',
    'production_manager',
    'quality_control_manager',
    'quality_control_inspector',
)

class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all().order_by('-created_at')
    permission_classes = [RoleWritePermission]
    required_roles = REPORTS_ROLES

    def get_serializer_class(self):
        return IssueListSerializer if self.action == 'list' else IssueDetailSerializer

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all().order_by('-created_at')
    permission_classes = [RoleWritePermission]
    required_roles = REPORTS_ROLES

    def get_serializer_class(self):
        return ReportListSerializer if self.action == 'list' else ReportDetailSerializer

class ReportTemplateViewSet(viewsets.ModelViewSet):
    queryset = ReportTemplate.objects.all()
    serializer_class = ReportTemplateSerializer
    permission_classes = [RoleWritePermission]
    required_roles = REPORTS_ROLES

class ScheduledReportViewSet(viewsets.ModelViewSet):
    queryset = ScheduledReport.objects.all()
    serializer_class = ScheduledReportSerializer
    permission_classes = [RoleWritePermission]
    required_roles = REPORTS_ROLES

class ProductionPerformanceReportAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            now = timezone.now()
            lines = ProductionLine.objects.annotate(
                total_orders=Count('productionorder'),
                completed_orders=Count('productionorder', filter=Q(productionorder__status='Completed')),
                average_duration=Avg(Cast(
                    F('productionorder__end_date') - F('productionorder__start_date'),
                    output_field=models.DurationField()
                )),
                delayed_orders=Count('productionorder',
                                   filter=Q(productionorder__end_date__lt=now) &
                                           ~Q(productionorder__status='Completed'))
            )

            report_data = []
            for line in lines:
                total = line.total_orders or 0
                completed = line.completed_orders or 0
                average_duration = line.average_duration
                if isinstance(average_duration, str):
                    average_duration = parse_duration(average_duration)
                elif isinstance(average_duration, (int, float)):
                    average_duration = timedelta(microseconds=average_duration)
                report_data.append({
                    'production_line': line.line_name,
                    'total_orders': total,
                    'completed_orders': completed,
                    'completion_rate': round(completed * 100.0 / total, 2) if total else 0,
                    'average_duration': average_duration,
                    'delayed_orders': line.delayed_orders or 0
                })

            serializer = ProductionPerformanceReportSerializer(
                report_data, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class WorkflowAnalysisReportAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            workflows = Workflow.objects.annotate(
                total_stages=Count('stages'),
                avg_stage_duration=Avg('stages__duration'),
                total_inspection_points=Count('stages__inspection_checkpoints')
            ).prefetch_related('stages')
            
            report_data = []
            for workflow in workflows:
                longest_stage = workflow.stages.order_by('-duration').first()
                
                # Prepare context as a dictionary
                context = {
                    'workflow': workflow,
                    'total_stages': workflow.total_stages or 0,
                    'avg_stage_duration': int(workflow.avg_stage_duration) if workflow.avg_stage_duration else 0,
                    'total_inspection_points': workflow.total_inspection_points or 0,
                    'longest_stage': longest_stage
                }
                
                # Initialize serializer with the context dictionary
                serializer = WorkflowAnalysisReportSerializer(context)
                report_data.append(serializer.data)
                
            return Response(report_data)
        
        except Exception as e:
            return Response(
                {'error': f"Report generation failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ProductionOrderStatusReportAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            status_data = ProductionOrder.objects.values('status').annotate(
                count=Count('id'),
                total_quantity=Sum('quantity')
            ).order_by('-count')
            
            # Convert QuerySet to list of dicts
            data_list = list(status_data)
            
            serializer = ProductionOrderStatusSerializer(data_list, many=True)
            return Response(serializer.data)
        
        except Exception as e:
            return Response(
                {'error': f"Failed to generate order status report: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class StageDurationReportAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, workflow_id=None, *args, **kwargs):
        try:
            queryset = Stage.objects.all()
            if workflow_id:
                queryset = queryset.filter(workflow_id=workflow_id)
                
            duration_data = queryset.values(
                'workflow__name', 
                'name'
            ).annotate(
                avg_duration=Avg('duration'),
                min_duration=Min('duration'),
                max_duration=Max('duration')
            ).order_by('workflow__name', 'avg_duration')
            
            # Convert ValuesQuerySet to list of dicts
            data_list = list(duration_data)
            
            serializer = StageDurationSerializer(data_list, many=True)
            return Response(serializer.data)
        
        except Exception as e:
            return Response(
                {'error': f"Failed to generate stage durations report: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ExportProductionReportAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, report_format=None, *args, **kwargs):
        try:
            lines = ProductionLine.objects.annotate(
                total_orders=Count('productionorder'),
                completed_orders=Count('productionorder', filter=Q(productionorder__status='Completed'))
            ).values('line_name', 'total_orders', 'completed_orders')
            
            df = pd.DataFrame.from_records(lines)
            
            if report_format == 'excel':
                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df.to_excel(writer, sheet_name='Production Report')
                output.seek(0)
                
                response = HttpResponse(
                    output.getvalue(),
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
                response['Content-Disposition'] = 'attachment; filename=production_report.xlsx'
                return response
                
            elif report_format == 'csv':
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename=production_report.csv'
                df.to_csv(response, index=False)
                return response
            
            return Response({"error": "Invalid format"}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)