from django.urls import path
from . import views

urlpatterns = [
    path('combine/', views.combine_items, name='combine_items'),
    path('user/', views.get_user, name='get_user'),
]
