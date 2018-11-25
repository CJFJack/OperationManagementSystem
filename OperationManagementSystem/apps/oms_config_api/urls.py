# -*- encoding: utf-8 -*-

from django.conf.urls import url
from . import views

app_name = 'oms_config_api'

urlpatterns = [
    url(r'^api_get_example/$', views.APIGetExample.as_view(), name='api_get_example'),
    url(r'^api_post_example/$', views.APIPostExample.as_view(), name='api_post_example'),
    url(r'^deploy_config/$', views.DeployConfig.as_view(), name='deploy_config'),
]
