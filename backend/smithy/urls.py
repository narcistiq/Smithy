from django.urls import path
from . import views

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),
    path('auth/logout/', views.logout, name='logout'),
    path('auth/profile/', views.get_user_profile, name='get_user_profile'),
    
    # Game endpoints
    path('combine/', views.combine_items, name='combine_items'),
    path('user/', views.get_user, name='get_user'),
]
