# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, reverse
from OperationManagementSystem.apps.deploy.models import DeployApply
from OperationManagementSystem.apps.deploy.forms import DeployApplyForm, DeployItemFormSet
from OperationManagementSystem.apps.operation.models import DeployECS
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime
import json

app_name = 'deploy'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class DeployApplyListView(generic.ListView):
    model = DeployApply
    template_name = 'deploy/apply_manage.html'
    context_object_name = 'apply_manage'

    def get_queryset(self):
        apply_manage = DeployApply.objects.order_by('-apply_time')
        return apply_manage


@login_required(login_url='/login/')
def deploy_apply_delete(request, apply_id):
    deploy_apply = DeployApply.objects.get(pk=apply_id)
    deploy_apply.delete()
    return HttpResponse(json.dumps({'success': True}), content_type='application/json')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class DeployApplyCreateView(generic.CreateView):
    template_name = 'deploy/apply_create.html'
    model = DeployApply
    form_class = DeployApplyForm
    success_url = '/deploy/apply_manage/'

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        deploy_apply_form = self.get_form(form_class)
        deploy_item_form = DeployItemFormSet()
        return self.render_to_response(
            self.get_context_data(deploy_apply_form=deploy_apply_form,
                                  deploy_item_form=deploy_item_form))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        deploy_apply_form = self.get_form(form_class)
        deploy_item_form = DeployItemFormSet(self.request.POST)
        if (deploy_apply_form.is_valid()
                and deploy_item_form.is_valid()):
            return self.form_valid(deploy_apply_form, deploy_item_form)
        else:
            return self.form_invalid(deploy_apply_form, deploy_item_form)

    def form_valid(self, deploy_apply_form, deploy_item_form):
        self.object = deploy_apply_form.save()
        deploy_item_form.instance = self.object
        deploy_item_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, deploy_apply_form, deploy_item_form):
        return self.render_to_response(
            self.get_context_data(deploy_apply_form=deploy_apply_form,
                                  deploy_item_form=deploy_item_form))
