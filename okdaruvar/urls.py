"""okdaruvar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from  . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('trainings/',include('trainings.urls')),
    path('',views.login_view, name='index'),
    path('logout/',views.logout_view, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('forgot-password/', views.forgot_password_view, name='forgot-password'),
    path('recover-password/', views.recover_password_view, name='recover-password'),
    path('change-password/', views.changed_password_view, name='change-password')
  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
