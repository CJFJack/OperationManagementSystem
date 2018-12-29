# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

app_name = 'mychannels'

urlpatterns = [
    url(r'^config_deploy_record/$', views.config_deploy_record, name='config_deploy_record'),
]
