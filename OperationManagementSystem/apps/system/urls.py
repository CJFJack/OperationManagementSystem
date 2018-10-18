# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

app_name = 'system'


urlpatterns = [
    url(r'^ecs/$', views.ECSListView.as_view(), name='ecs_manage'),
    url(r'^sync_all_ecs_from_acs/$', views.sync_all_ecs_from_acs, name='sync_all_ecs_from_acs'),
    url(r'^update_all_ecs_info/$', views.update_all_ecs_info, name='update_all_ecs_info'),
    url(r'^ecs_table_refresh/$', views.ecs_table_refresh, name='ecs_table_refresh'),
    url(r'^update_all_ecs_monitor/$', views.update_all_ecs_monitor, name='update_all_ecs_monitor'),
    url(r'^application/$', views.ApplicationListView.as_view(), name='application_manage'),
    url(r'^application_add/$', views.ApplicationAdd.as_view(), name='application_add'),
    url(r'^application_race/$', views.ApplicationRaceListView.as_view(), name='application_race'),
    url(r'^application_race_add/$', views.application_race_add, name='application_race_add'),
    url(r'^application_delete/(?P<application_id>[0-9]+)/$', views.application_delete, name='application_delete'),
]