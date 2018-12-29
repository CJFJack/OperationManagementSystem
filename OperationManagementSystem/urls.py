"""OperationManagementSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views
from OperationManagementSystem.apps.dashboard.views import alarm_charts

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^system/', include('OperationManagementSystem.apps.system.urls')),
    url(r'^config/', include('OperationManagementSystem.apps.config.urls')),
    url(r'^operation/', include('OperationManagementSystem.apps.operation.urls')),
    url(r'^alarm/', include('OperationManagementSystem.apps.alarm.urls')),
    url(r'^dashboard/', include('OperationManagementSystem.apps.dashboard.urls')),
    url(r'^deploy/', include('OperationManagementSystem.apps.deploy.urls')),
    url(r'^oms_config_api/', include('OperationManagementSystem.apps.oms_config_api.urls')),
    url(r'^mychannels/', include('OperationManagementSystem.apps.mychannels.urls')),
    url(r'^$', alarm_charts, name='index'),
    url(r'^login/', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
]
