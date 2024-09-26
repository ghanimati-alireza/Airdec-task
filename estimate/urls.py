from django.urls import path
from .views import EstimateCreateView, EstimateDetailView

urlpatterns = [
    path('', EstimateCreateView.as_view(), name='create-estimate'),
    path('<int:pk>/', EstimateDetailView.as_view(), name='estimate-detail'),
]