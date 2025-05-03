from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'issues', views.IssueViewSet, basename='issue')
router.register(r'reports', views.ReportViewSet, basename='report')
router.register(r'templates', views.ReportTemplateViewSet, basename='reporttemplate')
router.register(r'scheduled', views.ScheduledReportViewSet, basename='scheduledreport')

# Report endpoints
urlpatterns = [
    path('', include(router.urls)),
    path('production/performance/', views.ProductionPerformanceReportAPI.as_view(), 
        name='production-performance'),
    path('workflow/analysis/', views.WorkflowAnalysisReportAPI.as_view(), 
        name='workflow-analysis'),
    path('orders/status/', views.ProductionOrderStatusReportAPI.as_view(), 
        name='order-status'),
    path('stages/durations/', views.StageDurationReportAPI.as_view(), 
        name='stage-durations'),
    path('stages/durations/<int:workflow_id>/', views.StageDurationReportAPI.as_view(), 
        name='workflow-stage-durations'),
    path('export/production/<str:format>/', views.ExportProductionReportAPI.as_view(), 
        name='export-production'),
]