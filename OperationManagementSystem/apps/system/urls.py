# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views


app_name = 'system'

urlpatterns = [
    # ECS
    url(r'^ecs/$', views.ECSListView.as_view(), name='ecs_manage'),
    url(r'^sync_all_ecs_from_acs/$', views.sync_all_ecs_from_acs, name='sync_all_ecs_from_acs'),
    url(r'^update_all_ecs_info/$', views.update_all_ecs_info, name='update_all_ecs_info'),
    url(r'^ecs_table_refresh/$', views.ecs_table_refresh, name='ecs_table_refresh'),
    url(r'^update_all_ecs_monitor/$', views.update_all_ecs_monitor, name='update_all_ecs_monitor'),
    # Application Race
    url(r'^application_race/$', views.ApplicationRaceListView.as_view(), name='application_race'),
    url(r'^application_race_add/$', views.application_race_add, name='application_race_add'),
    url(r'^application_race_edit/(?P<pk>[0-9]+)/$', views.ApplicationRaceEditView.as_view(),
        name='application_race_edit'),
    url(r'^application_race_save/(?P<application_race_id>[0-9]+)/$', views.application_race_save,
        name='application_race_save'),
    url(r'^application_race_delete/(?P<application_race_id>[0-9]+)/$', views.application_race_delete,
        name='application_race_delete'),
    # Application
    url(r'^application/$', views.ApplicationListView.as_view(), name='application_manage'),
    url(r'^application_add/$', views.ApplicationAdd.as_view(), name='application_add'),
    url(r'^application_delete/(?P<application_id>[0-9]+)/$', views.application_delete, name='application_delete'),
    url(r'^application_change/(?P<pk>[0-9]+)/$', views.ApplicationChangeView.as_view(),
        name='application_change'),
    url(r'^application_save/(?P<application_id>[0-9]+)/$', views.application_save, name='application_save'),
    # slb
    url(r'^slb_manage/$', views.SLBListView.as_view(), name='slb_manage'),
    url(r'^sync_all_slb_from_acs/$', views.update_all_slb_info, name='sync_all_slb_from_acs'),
    url(r'^one_slb_health_update/(?P<slb_id>[0-9]+)/$', views.one_slb_health_update, name='one_slb_health_update'),
    url(r'^all_slb_health_update/$', views.all_slb_health_update, name='all_slb_health_update'),
    url(r'^slb_add_backend_server/(?P<slb_id>[0-9]+)/(?P<server_id>[0-9]+)/$', views.slb_add_backend_server,
        name='slb_add_backend_server'),
    url(r'^slb_remove_backend_server/(?P<slb_id>[0-9]+)/(?P<server_id>[0-9]+)/$', views.slb_remove_backend_server,
        name='slb_add_backend_server'),
    url(r'^slb_change/(?P<slb_id>[0-9]+)$', views.SLBChangeView.as_view(), name='slb_change'),

]
