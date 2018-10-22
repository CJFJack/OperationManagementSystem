# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from OperationManagementSystem.apps.config.models import Configfile
from OperationManagementSystem.apps.system.models import Application
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ConfigfileListView(generic.ListView):
    model = Application
    template_name = 'config/config_manage.html'
    context_object_name = 'application_list'
