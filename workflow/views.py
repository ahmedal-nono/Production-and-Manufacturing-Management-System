from django.db.models import Count
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductionLineSerializer
from .models import ProductionLine
from .models import ProductionOrder
from .models import Rescheduling
from .serializers import ReschedulingSerializer
from .serializers import ProductionOrderSerializer
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import BOM, Product, Workflow, Stage, InspectionCheckpoint, WorkCenter
from .serializers import BOMSerializer, ProductSerializer, WorkflowSerializer, StageSerializer, InspectionCheckpointSerializer
from administration.permissions import RoleWritePermission

PRODUCTION_ROLES = ('admin', 'production_manager', 'production_planner')



class InspectionCheckpointViewSet(viewsets.ModelViewSet):
    queryset = InspectionCheckpoint.objects.all()
    serializer_class = InspectionCheckpointSerializer
    permission_classes = [RoleWritePermission]
    required_roles = PRODUCTION_ROLES

class BOMViewSet(viewsets.ModelViewSet):
    queryset = BOM.objects.prefetch_related('components').all()
    serializer_class = BOMSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ['name', 'product_code', 'version']
    permission_classes = [RoleWritePermission]
    required_roles = PRODUCTION_ROLES

# Workflow ViewSet (Searchable Workflow)
class WorkflowViewSet(viewsets.ModelViewSet):
    queryset = Workflow.objects.select_related(
        'assigned_work_center', 'product'
    ).prefetch_related(
        'stages',
        'stages__inspection_checkpoints',
        'stages__assigned_work_center',
    ).all()
    serializer_class = WorkflowSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ['name', 'description']
    permission_classes = [RoleWritePermission]
    required_roles = PRODUCTION_ROLES

    def create(self, request, *args, **kwargs):
        """
        Override the default create method to handle creation of Workflow with Stages.
        The Workflow is created along with its Stages, without Inspection Checkpoints.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            workflow = serializer.save()  # Create the Workflow and its Stages
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Product ViewSet (Handles Product CRUD with BOM and Workflow linked)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('bom', 'workflow').prefetch_related(
        'workflow__stages',
        'workflow__stages__inspection_checkpoints',
        'bom__components'
    ).all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'bom__status']
    permission_classes = [RoleWritePermission]
    required_roles = PRODUCTION_ROLES

    # Single endpoint to create the Product with BOM and Workflow
    def create(self, request, *args, **kwargs):
        """
        Overriding the default create method to handle creation of Product with BOM and Workflow.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Overriding the default update method to handle updating Product and its related BOM and Workflow.
        """
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Stage ViewSet (Handles Stage creation with Inspection Checkpoints)
class StageViewSet(viewsets.ModelViewSet):
    queryset = Stage.objects.select_related(
        'assigned_work_center', 'workflow'
    ).prefetch_related('inspection_checkpoints').all()
    serializer_class = StageSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)  # Enable filtering and searching
    search_fields = ['name', 'assigned_work_center__name', 'work_order']
    permission_classes = [RoleWritePermission]
    required_roles = PRODUCTION_ROLES
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            stage = serializer.save()  # Save Stage and its associated Inspection Checkpoints
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductionLineViewSet(viewsets.ModelViewSet):
    queryset = ProductionLine.objects.prefetch_related('work_centers').all()
    serializer_class = ProductionLineSerializer
    permission_classes = [RoleWritePermission]
    required_roles = PRODUCTION_ROLES



class ProductionOrderViewSet(viewsets.ModelViewSet):
    queryset = ProductionOrder.objects.select_related(
        'product', 'production_line'
    ).prefetch_related('work_orders').annotate(
        work_orders_total=Count('work_orders')
    ).all()
    serializer_class = ProductionOrderSerializer
    permission_classes = [RoleWritePermission]
    required_roles = PRODUCTION_ROLES



class ReschedulingViewSet(viewsets.ModelViewSet):
    queryset = Rescheduling.objects.select_related('production_order').all()
    serializer_class = ReschedulingSerializer
    permission_classes = [RoleWritePermission]
    required_roles = PRODUCTION_ROLES