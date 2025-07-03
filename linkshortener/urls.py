from django.contrib import admin
from django.urls import path, include
from shortener import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shortener.urls')),    
    path('<str:code>/', views.redirect_short_code, name='redirect'),
]
