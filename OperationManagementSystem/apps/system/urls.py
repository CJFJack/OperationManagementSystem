# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

app_name = 'system'


urlpatterns = [
    url(r'^ecs/$', views.ECSListView.as_view(), name='ecs_manage'),
    url(r'^sync_all_ecs_from_acs/$', views.sync_all_ecs_from_acs, name='sync_all_ecs_from_acs')
]