from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkOrderViewSet, JobCardViewSet, WorkInstructionViewSet

router = DefaultRouter()
router.register(r'work_orders', WorkOrderViewSet)
router.register(r'job_cards', JobCardViewSet)
router.register(r'work_instructions', WorkInstructionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
