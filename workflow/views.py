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



class InspectionCheckpointViewSet(viewsets.ModelViewSet):
    queryset = InspectionCheckpoint.objects.all()
    serializer_class = InspectionCheckpointSerializer
    permission_classes = []  # No permission required for this viewset

class BOMViewSet(viewsets.ModelViewSet):
    queryset = BOM.objects.all()
    serializer_class = BOMSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ['name', 'product_code', 'version']
    permission_classes = [] 

# Workflow ViewSet (Searchable Workflow)
class WorkflowViewSet(viewsets.ModelViewSet):
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ['name', 'description']
    permission_classes = [] 

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
    queryset = Product.objects.select_related('bom', 'workflow').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'bom__status']
    permission_classes = [] 

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
    queryset = Stage.objects.all()
    serializer_class = StageSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)  # Enable filtering and searching
    search_fields = ['name', 'assigned_work_center__name', 'work_order']
    permission_classes = [] 
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            stage = serializer.save()  # Save Stage and its associated Inspection Checkpoints
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductionLineViewSet(viewsets.ModelViewSet):
    queryset = ProductionLine.objects.all()
    serializer_class = ProductionLineSerializer
    permission_classes = [] 



class ProductionOrderViewSet(viewsets.ModelViewSet):
    queryset = ProductionOrder.objects.all()
    serializer_class = ProductionOrderSerializer
    permission_classes = [] 



class ReschedulingViewSet(viewsets.ModelViewSet):
    queryset = Rescheduling.objects.all()
    serializer_class = ReschedulingSerializer
    permission_classes = [] 