from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/active-employees/', views.api_active_employees, name='api_active_employees'),
    path('api/pending-recertifications/', views.api_pending_recertifications, name='api_pending_recertifications'),
    path('api/recertify/', views.api_recertify, name='api_recertify'),
]
