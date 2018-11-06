# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

app_name = 'deploy'

urlpatterns = [
    url(r'^apply_manage/$', views.DeployApplyListView.as_view(), name='apply_manage'),
    url(r'^apply_add/$', views.DeployApplyAddView.as_view(), name='apply_add'),
]
