# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

app_name = 'jenkins'

urlpatterns = [
    url(r'^jenkins_job_list/$', views.JenkinsJobListView.as_view(), name='jenkins_job_list'),
    url(r'^build/(?P<job_id>[0-9]+)/$', views.build, name='build'),
]
