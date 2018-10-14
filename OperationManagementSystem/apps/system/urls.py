# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^base/$', views.base, name='base'),
    url(r'^ecs/$', views.ECSListView.as_view(), name='ecs_manage')
]