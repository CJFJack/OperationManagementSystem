# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

app_name = 'operation'

urlpatterns = [
    url(r'^config_deploy/(?P<release_id>[0-9]+)/$', views.config_deploy, name='config_deploy'),
]
