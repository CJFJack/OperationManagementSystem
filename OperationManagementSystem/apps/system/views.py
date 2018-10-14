# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import generic
from OperationManagementSystem.apps.system.models import ECS
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def base(request):
    return render(request, '__base__.html', {})


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ECSListView(generic.ListView):
    model = ECS
    template_name = 'system/ecs_manage.html'
    context_object_name = 'ecs_manage'

    def get_queryset(self):
        return ECS.objects.order_by('name')
