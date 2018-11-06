# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, reverse
from OperationManagementSystem.apps.deploy.models import DeployApply
from OperationManagementSystem.apps.deploy.forms import DeployItemFormSet
from django.views import generic, View
from .forms import DeployApplyForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect


app_name = 'deploy'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class DeployApplyListView(generic.ListView):
    model = DeployApply
    template_name = 'deploy/apply_manage.html'
    context_object_name = 'apply_manage'

    def get_queryset(self):
        apply_manage = DeployApply.objects.order_by('-apply_time')
        return apply_manage


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class DeployApplyAddView(View):
    def get(self, request):
        deploy_item_formset = DeployItemFormSet()
        return render(request, 'deploy/apply_add.html', {'deploy_item_formset': deploy_item_formset})

    def post(self, request):
        deploy_apply_form = DeployApplyForm(request.POST)
        deploy_item_formset = DeployItemFormSet()
        if deploy_apply_form.is_valid():
            deploy_apply_form.save(commit=False)
            deploy_apply_form.save()
        else:
            return render(request, 'deploy/apply_add.html', {'deploy_apply_form': deploy_apply_form,
                                                             'deploy_item_formset': deploy_item_formset})
        return HttpResponseRedirect(reverse('deploy:apply_manage'))
