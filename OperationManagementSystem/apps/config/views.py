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
    """修改相关配置文件，并更新配置文件发布状态"""
    if "log" in configfile.filename:
        """log配置文件处理"""
        configfile.modified_user = request.user.username
        configfile.content = request.POST['content']
        configfile.save()
        for r in configfile.application.release_set.all():
            r.status = "N"
            r.save()
    else:
        """非log配置文件处理"""
        for application_obj in configfile.get_application_race_application_list():
            for configfile_obj in application_obj.configfile_set.all():
                if configfile_obj.filename == configfile.filename:
                    configfile_obj.modified_user = request.user.username
                    configfile_obj.content = request.POST['content']
                    configfile_obj.save()
            for r in application_obj.release_set.all():
                r.status = "N"
                r.save()
    return HttpResponseRedirect(reverse('config:configfile'))





