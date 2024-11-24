from django.urls import path
from .views import CompanyDetailView, CompanyCreateView

urlpatterns = [
    path('api/companies/', CompanyCreateView.as_view(), name='create_company'),
    path('api/companies/<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),
]
