# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.views import generic
from OperationManagementSystem.apps.system.models import ECS
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from acs_api.acs_sync_all_ecs import sync_all_ecs
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

import json

app_name = 'system'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ECSListView(generic.ListView):
    model = ECS
    template_name = 'system/ecs_manage.html'
    context_object_name = 'ecs_manage'

    def get_queryset(self):
        return ECS.objects.order_by('name')


@login_required(login_url='/login/')
def sync_all_ecs_from_acs(request):
    ecs_acs = sync_all_ecs(region_id='cn-hangzhou')
    ecs_local = []
    '''获取本地所有ecs实例id的list'''
    for ecs in ECS.objects.all():
        ecs_local.append(ecs.instanceid)
    '''增加本地没有的ecs'''
    for ecs_instance_id in ecs_acs:
        if ecs_instance_id not in ecs_local:
            ecs = ECS(instanceid=ecs_instance_id)
            ecs.save()
    '''删除阿里云没有的本地ecs'''
    for ecs_instance_id in ecs_local:
        if ecs_instance_id not in ecs_acs:
            ecs = get_object_or_404(ECS, instanceid=ecs_instance_id)
            ecs.delete()
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")
