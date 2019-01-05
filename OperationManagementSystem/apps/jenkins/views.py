# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views import generic
from .models import JenkinsJobList, JenkinsBuildHistory
from django.http import JsonResponse
from OperationManagementSystem.apps.jenkins.utils import jenkins_build
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

app_name = 'jenkins'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class JenkinsJobListView(generic.ListView):
    model = JenkinsJobList
    context_object_name = 'jenkins_list'
    template_name = 'jenkins/jenkins_job_list.html'


@login_required(login_url='/login/')
@csrf_exempt
def build(request, job_id):
    result = jenkins_build(job_id, params={'min': 2})
    if result['success']:
        return JsonResponse({'data': True, 'msg': ''})
    else:
        return JsonResponse({'data': False, 'msg': result['msg']})


@login_required(login_url='/login/')
def job_history(request, job_id):
    job_history = JenkinsBuildHistory.objects.filter(job_id=job_id).order_by('-build_no')
    if job_history:
        return render(request, 'jenkins/jenkins_job_history.html', {'job_history': job_history})
    else:
        return render(request, 'jenkins/jenkins_job_history.html', {})
