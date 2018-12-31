# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, reverse
from django.views import generic
from .models import JenkinsJobList

app_name = 'jenkins'


class JenkinsJobListView(generic.ListView):
    model = JenkinsJobList
    context_object_name = 'jenkins_list'
    template_name = 'jenkins/jenkins_job_list.html'
