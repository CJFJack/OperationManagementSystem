# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.views import generic
from OperationManagementSystem.apps.system.models import ECS, Application, ApplicationRace
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from acs_api.acs_sync_all_ecs import sync_all_ecs
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from acs_api.acs_update_ecs_info import update_ecs_info
from django.shortcuts import render, reverse
from acs_api.acs_update_ecs_monitor import update_ecs_monitor
from OperationManagementSystem.apps.system.forms import ApplicationForm

import json
import random
import time

app_name = 'system'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ECSListView(generic.ListView):
    model = ECS
    template_name = 'system/ecs_manage.html'
    context_object_name = 'ecs_manage'

    def get_queryset(self):
        return ECS.objects.order_by('name')


@login_required(login_url='/login/')
@csrf_exempt
def sync_all_ecs_from_acs(request):
    ecs_acs = sync_all_ecs(region_id='cn-hangzhou')
    ecs_local = []
    '''获取本地所有ecs实例id的list'''
    for ecs in ECS.objects.all():
        ecs_local.append(ecs.instance_id)
    '''增加本地没有的ecs'''
    for ecs_instance_id in ecs_acs:
        if ecs_instance_id not in ecs_local:
            ecs = ECS(instance_id=ecs_instance_id)
            ecs.save()
    '''删除阿里云没有的本地ecs'''
    for ecs_instance_id in ecs_local:
        if ecs_instance_id not in ecs_acs:
            ecs = get_object_or_404(ECS, instance_id=ecs_instance_id)
            ecs.delete()
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


def update_one_ecs_info(request, ecs_id):
    ecs = get_object_or_404(ECS, pk=ecs_id)
    instance_id = ecs.instance_id.encode('utf-8')
    try:
        result = update_ecs_info(instance_id=[instance_id])
    except:
        pass
    else:
        ecs.instance_status = result['Status']
        ecs.IP = result['InnerIpAddress']
        ecs.public_ip_address = result['PublicIpAddress']
        ecs.regionId = result['RegionId']
        ecs.osname = result['OSName']
        ecs.expired_time = result['ExpiredTime']
        ecs.memory = result['Memory'] / 1024
        ecs.os_type = result['OSType']
        ecs.network_type = result['NetworkType']
        ecs.name = result['InstanceName']
        ecs.cpu = result['Cpu']
        ecs.save()

    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@login_required(login_url='/login/')
@csrf_exempt
def update_all_ecs_info(request):
    for ecs in ECS.objects.all():
        update_one_ecs_info(request, ecs.id)
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@login_required(login_url='/login/')
@csrf_exempt
def ecs_table_refresh(request):
    ecs_manage = ECS.objects.order_by('name')
    template = 'system/ecs_table_data.html'
    return render(request, template, {'ecs_manage': ecs_manage})


def update_one_ecs_monitor(request, ecs_id):
    ecs = get_object_or_404(ECS, pk=ecs_id)
    instance_id = ecs.instance_id.encode('utf-8')
    try:
        recently_cpu = update_ecs_monitor(instance_id=instance_id, metric="cpu_total")
        recently_mem = update_ecs_monitor(instance_id=instance_id, metric="memory_usedutilization")
        recently_disk_usage = update_ecs_monitor(instance_id=instance_id, metric="diskusage_utilization")
    except:
        pass
    else:
        ecs.recently_memory = recently_mem['Average']
        ecs.recently_cpu = recently_cpu['Average']
        ecs.recently_disk_usage = recently_disk_usage['Average']
        ecs.save()

    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@login_required(login_url='/login/')
@csrf_exempt
def update_all_ecs_monitor(request):
    for ecs in ECS.objects.all():
        update_one_ecs_monitor(request, ecs.id)
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ApplicationListView(generic.ListView):
    model = Application
    template_name = 'system/application_manage.html'
    context_object_name = 'application_manage'

    def get_queryset(self):
        return Application.objects.order_by('fullname')


@login_required(login_url='/login/')
def application_delete(request, application_id):
    application = Application.objects.get(pk=application_id)
    application.delete()
    return HttpResponse(json.dumps({'success': True}), content_type='application/json')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ApplicationAdd(generic.View):
    def get(self, request):
        ecs_list = ECS.objects.all()
        application_race_list = ApplicationRace.objects.all()
        return render(request, 'system/application_add.html', {'ecs_list': ecs_list,
                                                               'application_race_list': application_race_list})

    def post(self, request):
        application_form = ApplicationForm(request.POST)
        if application_form.is_valid():
            """保存应用基本信息"""
            application_form.save(commit=False)
            random_id = random.randint(10000000, 99999999)
            application_form.instance.random_id = random_id
            application_form.save()
            """实例化"""
            application = Application.objects.get(random_id=random_id)
            """添加关联配置文件"""
            config_files_list = request.POST['config_files'].split(';')
            if config_files_list:
                for config_file in config_files_list:
                    application.configfile_set.create(filename=config_file)
            """添加关联ECS"""
            application.modified_user = request.user.username
            ecs_id_list = request.POST.getlist('select_ecs[]', '')
            if ecs_id_list:
                for ecs_id in ecs_id_list:
                    ecs_obj = ECS.objects.get(name=ecs_id)
                    application.ECS_lists.add(ecs_obj)
            """添加应用族"""
            application_race_id = request.POST['select_application_race']
            application.application_race_id = int(application_race_id)
            """保存"""
            application.save()
            return HttpResponseRedirect(reverse('system:application_manage'))
        else:
            return render(request, 'system/application_manage.html', {'application_form': application_form})


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ApplicationRaceListView(generic.ListView):
    model = ApplicationRace
    template_name = 'system/application_race.html'
    context_object_name = 'application_race_list'


@login_required(login_url='/login/')
@csrf_exempt
def application_race_add(request):
    random_id = int(round(time.time() * 1000))
    application_race = ApplicationRace(race_id=random_id)
    application_race.save()
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ApplicationChangeView(generic.DetailView):
    model = Application
    template_name = 'system/application_change.html'

    def get_context_data(self, **kwargs):
        context = super(ApplicationChangeView, self).get_context_data(**kwargs)
        ecs_list = ECS.objects.all()
        application_race_list = ApplicationRace.objects.all()
        context['ecs_list'] = ecs_list
        context['application_race_list'] = application_race_list
        return context


@login_required(login_url='/login/')
def application_save(request, application_id):
    application_form = ApplicationForm(request.POST, instance=Application.objects.get(pk=application_id))
    application_form.save(commit=True)
    """实例化"""
    application = Application.objects.get(pk=application_id)
    """更新所属配置文件"""
    config_files_list = request.POST['config_files'].split(';')
    if config_files_list:
        for config_file in config_files_list:
            if config_file in application.get_config_files_name_list():
                pass
            else:
                application.configfile_set.create(filename=config_file)
    for config_file in application.get_config_files_name_list():
        if config_file in config_files_list:
            pass
        else:
            a = application.configfile_set.get(filename=config_file)
            a.delete()
    """修改所属ECS"""
    ecs_id_list = request.POST.getlist('select_ecs[]', '')
    if ecs_id_list:
        for ecs_id in ecs_id_list:
            if ecs_id in application.get_ecs_id_list():
                pass
            else:
                ecs_obj = ECS.objects.get(pk=int(ecs_id))
                application.ECS_lists.add(ecs_obj)
    # print application.get_ecs_id_list()
    for ecs_id in application.get_ecs_id_list():
        if ecs_id in ecs_id_list:
            pass
        else:
            ecs_obj = ECS.objects.get(pk=int(ecs_id))
            application.ECS_lists.remove(ecs_obj)
    return HttpResponseRedirect(reverse('system:application_manage'))
