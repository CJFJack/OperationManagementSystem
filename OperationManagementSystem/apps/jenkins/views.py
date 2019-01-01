# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, reverse
from django.views import generic
from .models import JenkinsJobList
from django.http import JsonResponse
from OperationManagementSystem.tasks import jenkins_build
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

app_name = 'jenkins'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class JenkinsJobListView(generic.ListView):
    model = JenkinsJobList
    context_object_name = 'jenkins_list'
    template_name = 'jenkins/jenkins_job_list.html'


@login_required(login_url='/login/')
@csrf_exempt
def build(request, job_id):
    job = JenkinsJobList.objects.get(pk=job_id)
    job.status = 1
    job.save()
    result, reason = jenkins_build(job.name, job.id)
    reason = str(reason[0])
    if result:
        return JsonResponse({'data': True, 'msg': ''})
    else:
        return JsonResponse({'data': False, 'msg': reason})
