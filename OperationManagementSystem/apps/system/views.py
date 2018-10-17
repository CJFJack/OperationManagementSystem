# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.views import generic
from OperationManagementSystem.apps.system.models import ECS, Application
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from acs_api.acs_sync_all_ecs import sync_all_ecs
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from acs_api.acs_update_ecs_info import update_ecs_info
from django.shortcuts import render
from acs_api.acs_update_ecs_monitor import update_ecs_monitor
from OperationManagementSystem.apps.system.forms import ApplicationForm

import json, random

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


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ApplicationAdd(generic.View):
    def get(self, request):
        ecs_list = ECS.objects.all()
        random_id = random.randint(10000000, 99999999)
        return render(request, 'system/application_add.html', {'ecs_list': ecs_list, 'random_id': random_id})

    def post(self, request):
        application_form = ApplicationForm(request.POST)
        if application_form.is_valid():
            application_form.save(commit=True)
            application = Application.objects.get(random_id=request.POST['random_id'])
            application.modified_user = request.user.username
            ecs_list = request.POST.getlist('select_ecs[]', '')
            if ecs_list:
                for ecs in ecs_list:
                    ecs_obj = ECS.objects.get(name=ecs)
                    application.ECS_lists.add(ecs_obj)
            application.save()

            return render(request, 'system/application_manage.html', {})
        else:
            return render(request, 'system/application_manage.html', {'application_form': application_form})




