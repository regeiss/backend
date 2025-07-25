"""
URLs da API
"""
from django.urls import path
from .views import health_check, api_info, RegisterView, ProfileView

app_name = 'api'

urlpatterns = [
    path('', api_info, name='info'),
    path('health/', health_check, name='health'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),
]
