from django.urls import path
from . import views

urlpatterns = [
    # Custom login endpoint (formato customizado de resposta)
    path('login/', views.login_view, name='custom_login'),
    
    # User profile
    path('user/', views.user_profile_view, name='user_profile'),
    
    # Logout
    path('logout/', views.logout_view, name='logout'),
    
    # Change password
    path('change-password/', views.change_password_view, name='change_password'),
]
