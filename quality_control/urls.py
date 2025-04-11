from django.urls import path
from . import views

urlpatterns = [
    path('workorders/', views.WorkOrderListView.as_view()),
    path('workorders/<int:pk>/', views.WorkOrderDetailView.as_view()),
    path('inspections/', views.InspectionCreateView.as_view()),
    path('inspections/<int:pk>/', views.InspectionDetailView.as_view()),
    path('checklist/<int:pk>/', views.InspectionChecklistUpdateView.as_view()),
    path('rework-requests/', views.ReworkRequestListView.as_view()),
    path('rework-requests/<int:pk>/', views.ReworkRequestUpdateView.as_view()),
]
