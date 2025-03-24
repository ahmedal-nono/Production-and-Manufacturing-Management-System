# workflow/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, WorkflowViewSet, BOMViewSet, StageViewSet, InspectionCheckpointViewSet
from .views import ProductionLineViewSet, ProductionOrderViewSet, ReschedulingViewSet

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'workflows', WorkflowViewSet, basename='workflow')
router.register(r'boms', BOMViewSet, basename='bom')
router.register(r'stages', StageViewSet, basename='stage')
router.register(r'inspection-checkpoints', InspectionCheckpointViewSet, basename='inspection-checkpoint')
router.register(r'production-lines', ProductionLineViewSet)
router.register(r'production-orders', ProductionOrderViewSet)
router.register(r'rescheduling', ReschedulingViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
