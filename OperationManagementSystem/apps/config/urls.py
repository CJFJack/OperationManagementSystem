# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

app_name = 'config'

urlpatterns = [
    url(r'^configfile/$', views.ConfigfileListView.as_view(), name='configfile'),
]