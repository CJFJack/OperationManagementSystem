# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, reverse
from OperationManagementSystem.apps.config.models import Configfile
from OperationManagementSystem.apps.system.models import Application

from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ConfigfileListView(generic.ListView):
    model = Application
    template_name = 'config/config_manage.html'
    context_object_name = 'application_list'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ConfigChangeDetailView(generic.DetailView):
    model = Configfile
    template_name = 'config/config_change.html'

    def get_context_data(self, **kwargs):
        context = super(ConfigChangeDetailView, self).get_context_data(**kwargs)
        context['application_list'] = Application.objects.all()
        return context


@login_required(login_url='/login/')
def configfile_change_save(request, configfile_id):
    configfile = Configfile.objects.get(pk=configfile_id)
    configfile.modified_user = request.user.username
    configfile.content = request.POST['content']
    configfile.save()
    return HttpResponseRedirect(reverse('config:configfile'))





