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
        deploy_item_formset = DeployItemFormSet()
        return self.render_to_response(
            self.get_context_data(deploy_apply_form=deploy_apply_form,
                                  deploy_item_formset=deploy_item_formset))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        deploy_apply_form = self.get_form(form_class)
        deploy_apply_form.instance.apply_user = request.user.username
        deploy_item_formset = DeployItemFormSet(self.request.POST)
        if (deploy_apply_form.is_valid()
                and deploy_item_formset.is_valid()):
            return self.form_valid(request, deploy_apply_form, deploy_item_formset)
        else:
            return self.form_invalid(deploy_apply_form, deploy_item_formset)

    def form_valid(self, request, deploy_apply_form, deploy_item_formset):
        wish_deploy = deploy_apply_form.instance.wish_deploy_time
        if wish_deploy is not None:
            wish_deploy_date = datetime.strptime(str(wish_deploy), "%Y-%d-%m").strftime("%Y-%m-%d")
            deploy_apply_form.instance.wish_deploy_time = wish_deploy_date
        self.object = deploy_apply_form.save()
        deploy_item_formset.instance = self.object
        deploy_item_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, deploy_apply_form, deploy_item_formset):
        return self.render_to_response(
            self.get_context_data(deploy_apply_form=deploy_apply_form,
                                  deploy_item_formset=deploy_item_formset))


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class DeployApplyUpdateView(generic.UpdateView):
    template_name = 'deploy/apply_update.html'
    model = DeployApply
    form_class = DeployApplyForm

    def get_success_url(self):
        self.success_url = '/deploy/apply_manage/'
        return self.success_url

    def get_context_data(self, **kwargs):
        context = super(DeployApplyUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['deploy_apply_form'] = DeployApplyForm(self.request.POST, instance=self.object)
            context['deploy_item_formset'] = DeployItemFormSet(self.request.POST, instance=self.object)
        else:
            context['deploy_apply_form'] = DeployApplyForm(instance=self.object)
            context['deploy_item_formset'] = DeployItemFormSet(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        deploy_apply_form = self.get_form(form_class)
        deploy_item_formset = DeployItemFormSet(self.request.POST)
        if (deploy_apply_form.is_valid()
                and deploy_item_formset.is_valid()):
            return self.form_valid(deploy_apply_form, deploy_item_formset)
        else:
            return self.form_invalid(deploy_apply_form, deploy_item_formset)

    def form_valid(self, deploy_apply_form, deploy_item_formset):
        self.object = deploy_apply_form.save()
        deploy_item_formset.instance = self.object
        deploy_item_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, deploy_apply_form, deploy_item_formset):
        return self.render_to_response(
            self.get_context_data(deploy_apply_form=deploy_apply_form,
                                  deploy_item_formset=deploy_item_formset))
