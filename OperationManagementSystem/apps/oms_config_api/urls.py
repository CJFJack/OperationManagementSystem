# -*- encoding: utf-8 -*-

from django.conf.urls import url
from . import views

app_name = 'oms_config_api'

urlpatterns = [
    url(r'^list_users/$', views.ListUsers.as_view(), name='list_users'),
]
