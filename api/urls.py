from django.urls import path
from .views import get_orders, api, get_profiles

urlpatterns = [
    path('', api, name='api'),
    path('get_orders/', get_orders, name='get_orders'),
    path('get_profiles/', get_profiles, name='get_profiles')
]