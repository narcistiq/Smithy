from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/', views.register),
    path('auth/login/', views.login),
    path('auth/logout/', views.logout),

    path('auth/profile/', views.get_user_profile),

    path('combine/', views.combine_items),
    path('items/', views.get_all_items),
    path('recipes/', views.get_all_recipes),
]