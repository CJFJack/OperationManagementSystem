# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, reverse
from OperationManagementSystem.apps.deploy.models import DeployApply
from OperationManagementSystem.apps.deploy.forms import DeployItemFormSet
from OperationManagementSystem.apps.operation.models import DeployECS
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


# @method_decorator(login_required(login_url='/login/'), name='dispatch')
# class DeployApplyAddView(View):
#     def get(self, request):
#         deploy_item_formset = DeployItemFormSet()
#         return render(request, 'deploy/apply_add.html', {'deploy_item_formset': deploy_item_formset})
#
#     def post(self, request):
#         deploy_apply_form = DeployApplyForm(request.POST)
#         deploy_item_formset = DeployItemFormSet()
#         if deploy_apply_form.is_valid():
#             deploy_apply_form.save(commit=True)
#
#             obj = DeployApply.objects.get(pk=deploy_apply_form.instance.id)
#             deploy_item_formset = DeployItemFormSet(request.POST, request.FILES, instance=obj)
#             if deploy_item_formset.is_valid():
#                 deploy_item_formset.save(commit=True)
#             else:
#                 return render(request, 'deploy/apply_add.html', {'deploy_apply_form': deploy_apply_form,
#                                                                  'deploy_item_formset': deploy_item_formset})
#         else:
#             return render(request, 'deploy/apply_add.html', {'deploy_apply_form': deploy_apply_form,
#                                                              'deploy_item_formset': deploy_item_formset})
#
#         return HttpResponseRedirect(reverse('deploy:apply_manage'))


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class DeployApplyAdd(generic.CreateView):
    model = DeployApply
    fields = ('apply_project', 'wish_deploy_time', 'conf_amend_explain', 'remark_explain')
    template_name = 'deploy/apply_add.html'

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        deploy_item_form = DeployItemFormSet()
        return self.render_to_response(
            self.get_context_data(form=form, deploy_item_form=deploy_item_form))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        apply_form = self.get_form(form_class)
        deploy_item_form = DeployItemFormSet(self.request.POST)
        if (apply_form.is_valid() or deploy_item_form.is_valid()):
            return self.form_valid(apply_form, deploy_item_form)
        else:
            return self.form_invalid(apply_form, deploy_item_form)

    def form_valid(self, apply_form, deploy_item_form):
        apply_form.instance.apply_user = self.request.user
        self.object = apply_form.save()
        deploy_item_form.instance = self.object
        for form in deploy_item_form:
            try:
                application_id = form.cleaned_data['deploy_application'].id
            except:
                pass
            else:
                for ecs in form.cleaned_data['deploy_application'].ECSlists.all():
                    ecs_id = ecs.id
                    d = DeployECS(applyproject_id=apply_form.instance.id, ECS_id=ecs_id, application_id=application_id)
                    d.save()
                    deploy_item_form.save()
        return HttpResponseRedirect(reverse('deploy:apply_manage'))

    def form_invalid(self, apply_form, deploy_item_form):
        return self.render_to_response(
            self.get_context_data(apply_form=apply_form, deploy_item_form=deploy_item_form))