"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from django.contrib.auth import views as auth_views

from dashboard import views as dashboard_views

urlpatterns = [
    path('session_security/', include('session_security.urls')),
    path('', dashboard_views.home, name='home'),
    path('admin/', admin.site.urls, name='admin'),
    path('login/', auth_views.login, {'template_name': 'dashboard/login.html'}, name='login'),
    path('logout/', auth_views.logout, {'next_page': 'login'}, name='logout'),
    path('upload/', dashboard_views.upload_accounts, name="upload"),
	path('820transactions/',dashboard_views.transactions,name="820transactions")
]

handler404 = 'dashboard.views.view_404'
