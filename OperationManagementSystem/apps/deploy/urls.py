# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

app_name = 'deploy'

urlpatterns = [
    url(r'^apply_manage/$', views.DeployApplyListView.as_view(), name='apply_manage'),
    url(r'^apply_delete/(?P<apply_id>[0-9]+)/$', views.deploy_apply_delete, name='apply_delete'),
    url(r'^apply_create/$', views.DeployApplyCreateView.as_view(), name='apply_create'),
]
