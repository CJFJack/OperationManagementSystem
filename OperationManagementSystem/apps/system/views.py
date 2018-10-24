# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.views import generic
from OperationManagementSystem.apps.system.models import ECS, Application, ApplicationRace, SLB
from OperationManagementSystem.apps.operation.models import SLBToApplication
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from acs_api.acs_sync_all_ecs import sync_all_ecs
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from acs_api.acs_update_ecs_info import update_ecs_info
from acs_api.acs_sync_all_slb import sync_all_slb
from acs_api.acs_update_slb_health import update_slb_health
from acs_api.acs_slb_backend_server_add import add_backend_server
from acs_api.acs_slb_backend_server_remove import remove_backend_server
from django.shortcuts import render, reverse
from acs_api.acs_update_ecs_monitor import update_ecs_monitor
from OperationManagementSystem.apps.system.forms import ApplicationForm
from OperationManagementSystem.apps.operation.models import SLBHealthStatus

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
            """添加修改人信息"""
            application.modified_user = request.user.username
            """添加关联ECS，生成配置文件发布状态记录"""
            ecs_id_list = request.POST.getlist('select_ecs[]', '')
            if ecs_id_list:
                for ecs_id in ecs_id_list:
                    ecs_obj = ECS.objects.get(pk=ecs_id)
                    application.ECS_lists.add(ecs_obj)
                    application.release_set.create(ECS_id=ecs_id, application_id=application.id)
            """添加应用族"""
            application_race_id = request.POST['select_application_race']
            if application_race_id == "0":
                pass
            else:
                application.application_race_id = int(application_race_id)
                application.save()
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
    return HttpResponseRedirect(reverse('system:application_race'))


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
    """应用实例化"""
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
    """修改所属ECS，并更新配置文件发布状态记录"""
    ecs_id_list = request.POST.getlist('select_ecs[]', '')
    if ecs_id_list:
        for ecs_id in ecs_id_list:
            """添加所属ECS"""
            if ecs_id in application.get_ecs_id_list():
                pass
            else:
                ecs_obj = ECS.objects.get(pk=int(ecs_id))
                application.ECS_lists.add(ecs_obj)
            """添加配置文件发布状态记录"""
            if application.release_set.filter(ECS_id=ecs_id):
                pass
            else:
                application.release_set.create(ECS_id=ecs_id, application_id=application.id)
    """删除所属ECS"""
    for ecs_id in application.get_ecs_id_list():
        if ecs_id in ecs_id_list:
            pass
        else:
            ecs_obj = ECS.objects.get(pk=int(ecs_id))
            application.ECS_lists.remove(ecs_obj)
    """删除配置文件发布状态记录"""
    for r in application.release_set.all():
        if str(r.ECS_id) in ecs_id_list:
            pass
        else:
            r.delete()
    """修改所属应用族"""
    application_race_id = request.POST['select_application_race']
    if application_race_id == '0':
        application.application_race_id = None
    else:
        application.application_race_id = int(application_race_id)
    """保存对象"""
    application.save()
    """生成发布状态记录"""
    return HttpResponseRedirect(reverse('system:application_manage'))


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ApplicationRaceEditView(generic.DetailView):
    model = ApplicationRace
    template_name = 'system/application_race_edit.html'
    context_object_name = 'application_race'
    
    def get_context_data(self, **kwargs):
        context = super(ApplicationRaceEditView, self).get_context_data(**kwargs)
        application_list = Application.objects.all()
        context['application_list'] = application_list
        return context


@login_required(login_url='/login/')
def application_race_save(request, application_race_id):
    """实例化"""
    application_race = ApplicationRace.objects.get(pk=application_race_id)
    """保存应用族基本信息"""
    alias = request.POST['alias']
    application_race.alias = alias
    application_race.save()
    """更新应用族关联应用"""
    select_application_id = request.POST.getlist('select_application_id[]', '')
    if select_application_id:
        for application_id in select_application_id:
            if application_id in application_race.get_application_id_list():
                pass
            else:
                application_obj = Application.objects.get(pk=application_id)
                application_obj.application_race_id = application_race.id
                application_obj.save()
    for application_id in application_race.get_application_id_list():
        if application_id in select_application_id:
            pass
        else:
            application_obj = Application.objects.get(pk=application_id)
            application_obj.application_race_id = None
            application_obj.save()
    return HttpResponseRedirect(reverse('system:application_race'))


@login_required(login_url='/login/')
def application_race_delete(request, application_race_id):
    application_race = ApplicationRace.objects.get(pk=application_race_id)
    application_race.delete()
    return HttpResponse(json.dumps({'success': True}), content_type='application/json')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SLBListView(generic.ListView):
    model = SLB
    template_name = 'system/slb_manage.html'
    context_object_name = 'slb_list'


@login_required(login_url='/login/')
@csrf_exempt
def update_all_slb_info(request):
    slb_list = []
    try:
        result = sync_all_slb(region_id='cn-hangzhou')
    except:
        return HttpResponse(json.dumps({'success': False, 'message': '网络超时，调用阿里云接口失败'}),
                            content_type="application/json")
    else:
        if 'Message' in result:
            return HttpResponse(json.dumps({'success': False, 'message': result['Message']}),
                                content_type="application/json")
        else:
            for slb in result:
                '''新增或更新现有SLB'''
                if not SLB.objects.filter(instance_id=slb['LoadBalancerId']):
                    s = SLB(instance_id=slb['LoadBalancerId'], name=slb['LoadBalancerName'],
                            status=slb['LoadBalancerStatus'], ip=slb['Address'], address_type=slb['AddressType'],
                            create_date=slb['CreateTime'], network_type=slb['NetworkType'])
                    s.save()
                else:
                    s = SLB.objects.get(instance_id=slb['LoadBalancerId'])
                    s.instance_id = slb['LoadBalancerId']
                    s.name = slb['LoadBalancerName']
                    s.status = slb['LoadBalancerStatus']
                    s.ip = slb['Address']
                    s.address_type = slb['AddressType']
                    s.create_date = slb['CreateTime']
                    s.network_type = slb['NetworkType']
                    s.save()
                slb_list.append(slb['LoadBalancerId'])
            for current_slb in SLB.objects.all():
                '''删除阿里云没有的SLB'''
                if current_slb.instance_id not in slb_list:
                    current_slb.delete()
            return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@login_required(login_url='/login/')
@csrf_exempt
def one_slb_health_update(request, slb_id):
    try:
        '''判断SLB实例是否存在'''
        slb = get_object_or_404(SLB, pk=slb_id)
    except:
        return render_to_response(request.META['HTTP_REFERER'], {'success': False})
    else:
        try:
            '''判断调用阿里云接口是否成功'''
            result = update_slb_health(LoadBalancerId=slb.instance_id)
        except:
            return HttpResponse(json.dumps({'success': False, 'message': '网络超时，调用阿里云接口失败'}),
                                content_type="application/json")
        else:
            if 'Message' in result:
                '''判断调用阿里云是否返回报错信息'''
                return HttpResponse(json.dumps({'success': False, 'message': result['Message']}),
                                    content_type="application/json")
            else:
                '''无报错则开始处理返回数据'''
                for sh in SLBHealthStatus.objects.filter(SLB_id=slb.id):
                    '''先将该SLB下所属ECS状态更新为已移除'''
                    sh.SLBStatus = 'removed'
                    sh.save()
                for r in result:
                    try:
                        '''判断数据库中是否存在ECS，没有则需要先到ECS页面同步ECS信息'''
                        ecs = get_object_or_404(ECS, instance_id=r['ServerId'])
                    except:
                        return HttpResponse(json.dumps({'success': False, 'message': 'ECS不存在，请到ECS页面进行同步后再刷新SLB信息'}),
                                            content_type="application/json")
                    else:
                        '''判断数据库中该SLB是否有对应的后端服务器记录，没有则增加，有则更新'''
                        if not SLBHealthStatus.objects.filter(SLB_id=slb.id, ECS_id=ecs.id):
                            sh = SLBHealthStatus(SLB_id=slb.id, ECS_id=ecs.id, SLBStatus='added',
                                                 health_status=r['ServerHealthStatus'])
                            sh.save()
                        else:
                            sh = SLBHealthStatus.objects.get(SLB_id=slb.id, ECS_id=ecs.id)
                            sh.SLB_id = slb.id
                            sh.ECS_id = ecs.id
                            sh.SLBStatus = 'added'
                            sh.health_status = r['ServerHealthStatus']
                            sh.save()
                return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@login_required(login_url='/login/')
@csrf_exempt
def all_slb_health_update(request):
    for slb in SLB.objects.all():
        one_slb_health_update(request, slb_id=slb.id)
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@login_required(login_url='/login/')
@csrf_exempt
def slb_add_backend_server(request, slb_id, server_id):
    slb = get_object_or_404(SLB, pk=slb_id)
    slb_instance_id = slb.instance_id
    ecs = ECS.objects.get(pk=server_id)
    server_dict = {}
    server_list = []
    server_dict['ServerId'] = str(ecs.instance_id)
    server_dict['Weight'] = str(100)
    server_list.append(server_dict)
    backend_servers = json.dumps(server_list)
    try:
        result = add_backend_server(LoadBalancerId=slb_instance_id, BackendServers=backend_servers)
    except:
        return HttpResponse(json.dumps({'success': False, 'message': '网络超时，调用阿里云接口失败'}),
                            content_type="application/json")
    else:
        if 'Message' in result:
            return HttpResponse(json.dumps({'success': False, 'message': result['Message']}),
                                content_type="application/json")
        else:
            one_slb_health_update(request, slb.id)
            return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@login_required(login_url='/login/')
@csrf_exempt
def slb_remove_backend_server(request, slb_id, server_id):
    slb = get_object_or_404(SLB, pk=slb_id)
    slb_instance_id = slb.instance_id
    ecs = ECS.objects.get(pk=server_id)
    backend_servers = []
    backend_servers.append(ecs.instance_id)
    backend_servers = json.dumps(backend_servers)
    try:
        r = remove_backend_server(LoadBalancerId=slb_instance_id, BackendServers=backend_servers)
        print r
    except:
        return HttpResponse(json.dumps({'success': False, 'message': '网络超时，调用阿里云接口失败'}),
                            content_type="application/json")
    else:
        if 'Message' in r:
            return HttpResponse(json.dumps({'success': False, 'message': r['Message']}),
                                content_type="application/json")
        else:
            one_slb_health_update(request, slb.id)
            return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SLBChangeView(generic.View):
    def get(self, request, slb_id):
        slb = SLB.objects.get(pk=slb_id)
        application_list = Application.objects.all()
        return render(request, 'system/slb_change.html', {'slb': slb, 'application_list': application_list})

    def post(self, request, slb_id):
        slb = SLB.objects.get(pk=slb_id)
        select_application_id = request.POST.getlist('select_application[]', '')
        if select_application_id:
            for application_id in select_application_id:
                if SLBToApplication.objects.filter(application_id=application_id, SLB_id=slb.id):
                    pass
                else:
                    slb_to_application = SLBToApplication(application_id=application_id, SLB_id=slb.id)
                    slb_to_application.save()
        for application_id in slb.get_application_id_list():
            if str(application_id) in select_application_id:
                pass
            else:
                slb_to_application = SLBToApplication.objects.get(application_id=application_id, SLB_id=slb.id)
                slb_to_application.delete()
        return HttpResponseRedirect(reverse('system:slb_manage'))


