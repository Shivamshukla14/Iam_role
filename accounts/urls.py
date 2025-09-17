from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('sso/start/', views.sso_start, name='sso_start'),
    path('sso/callback/', views.sso_callback, name='sso_callback'),
    path('logout/', views.logout_view, name='logout'),
]
