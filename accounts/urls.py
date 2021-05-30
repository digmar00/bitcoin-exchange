from django.urls import path
from .views import sign_up
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', sign_up, name='sign_up'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout')
]
