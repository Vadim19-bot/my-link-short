from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='shortener/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='shortener/logged_out.html'), name='logout'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('profile/', views.user_profile, name='user_profile'),
    path('create/', views.create_link, name='create_link'),
    path('<str:code>/', views.redirect_short_code, name='redirect'),
]
