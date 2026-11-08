from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
# from administration import permissions
from .models import WorkCenter, Workstation, Maintenance
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import WorkCenterSerializer, WorkstationSerializer, MaintenanceSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Workstation
from .serializers import WorkstationSerializer
from administration.permissions import RoleWritePermission

WORKCENTRE_ROLES = ('admin', 'production_manager')

class WorkCenterViewSet(viewsets.ModelViewSet):
    queryset = WorkCenter.objects.all()
    serializer_class = WorkCenterSerializer
    permission_classes = [RoleWritePermission]
    required_roles = WORKCENTRE_ROLES
    
    




class WorkstationViewSet(viewsets.ViewSet):  # Using ViewSet instead of ModelViewSet
    queryset = Workstation.objects.all()  # Make sure this is defined
    permission_classes = [RoleWritePermission]
    required_roles = WORKCENTRE_ROLES
    
    def list(self, request):
        # Custom list logic
        work_center = request.query_params.get('work_center', None)
        
        if work_center:
            queryset = Workstation.objects.filter(work_center=work_center)
        else:
            queryset = Workstation.objects.all()
            
        serializer = WorkstationSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        # Custom retrieve logic
        try:
            workstation = Workstation.objects.get(pk=pk)
            serializer = WorkstationSerializer(workstation)
            return Response(serializer.data)
        except Workstation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request):
        # Custom create logic
        serializer = WorkstationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        # Custom update logic
        try:
            workstation = Workstation.objects.get(pk=pk)
        except Workstation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        serializer = WorkstationSerializer(workstation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk=None):
        try:
            workstation = Workstation.objects.get(pk=pk)
        except Workstation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = WorkstationSerializer(
            workstation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        # Custom delete logic
        try:
            workstation = Workstation.objects.get(pk=pk)
            workstation.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Workstation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    # You can also add custom actions
    @action(detail=True, methods=['get'])
    def custom_action(self, request, pk=None):
        try:
            Workstation.objects.get(pk=pk)
        except Workstation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # Your custom logic here
        return Response({'message': 'Custom action performed'})
# class WorkstationViewSet(viewsets.ModelViewSet):
#     queryset = Workstation.objects.all()
#     serializer_class = WorkstationSerializer
#     filter_backends = [DjangoFilterBackend]  # Enable filtering
#     filterset_fields = ['work_center']  # Allow filtering by work_center
#     permission_classes = [AllowAny]


# class WorkstationViewSet(viewsets.ModelViewSet):
#     queryset = Workstation.objects.all()
#     serializer_class = WorkstationSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['work_center']
#     permission_classes = [AllowAny]

#     # Customize the queryset based on request parameters or user
#     def get_queryset(self):
#         queryset = super().get_queryset()
        
#         # Example: Add additional filtering
#         status = self.request.query_params.get('status', None)
#         if status:
#             queryset = queryset.filter(status=status)
            
#         # Example: Order by a specific field
#         queryset = queryset.order_by('name')
        
#         return queryset

#     # Customize create method
#     def create(self, request, *args, **kwargs):
#         # You can modify the request data before creation
#         request.data['created_by'] = request.user.id if request.user.is_authenticated else None
        
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
        
#         # Custom response after creation
#         headers = self.get_success_headers(serializer.data)
#         return Response(
#             {
#                 'status': 'success',
#                 'data': serializer.data,
#                 'message': 'Workstation created successfully'
#             },
#             status=status.HTTP_201_CREATED,
#             headers=headers
#         )

#     # Customize update method
#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
        
#         # Add custom validation or modification here
#         if instance.is_locked and not request.user.is_superuser:
#             return Response(
#                 {'error': 'This workstation is locked and cannot be modified'},
#                 status=status.HTTP_403_FORBIDDEN
#             )
        
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)

#         return Response(
#             {
#                 'status': 'success',
#                 'data': serializer.data,
#                 'message': 'Workstation updated successfully'
#             }
#         )

#     # Add custom actions
#     @action(detail=True, methods=['post'])
#     def activate(self, request, pk=None):
#         workstation = self.get_object()
#         workstation.is_active = True
#         workstation.save()
#         return Response({'status': 'activated'})

#     @action(detail=True, methods=['post'])
#     def deactivate(self, request, pk=None):
#         workstation = self.get_object()
#         workstation.is_active = False
#         workstation.save()
#         return Response({'status': 'deactivated'})

#     @action(detail=False, methods=['get'])
#     def summary(self, request):
#         # Custom endpoint for summary statistics
#         total = self.get_queryset().count()
#         active = self.get_queryset().filter(is_active=True).count()
#         return Response({
#             'total_workstations': total,
#             'active_workstations': active,
#             'inactive_workstations': total - active
#         })

#     # You can override perform_create/perform_update for additional logic
#     def perform_create(self, serializer):
#         # Additional actions before saving
#         serializer.save()

#     def perform_destroy(self, instance):
#         # Custom delete logic
#         if instance.is_protected:
#             raise ValidationError("This workstation is protected and cannot be deleted")
#         instance.delete()
class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
    permission_classes = [RoleWritePermission]
    required_roles = WORKCENTRE_ROLES