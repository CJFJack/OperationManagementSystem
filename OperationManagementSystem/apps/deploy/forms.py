from django.forms.models import inlineformset_factory
from django.forms import ModelForm
from OperationManagementSystem.apps.deploy.models import DeployApply
from OperationManagementSystem.apps.operation.models import DeployItem


class DeployApplyForm(ModelForm):
    class Meta:
        model = DeployApply
        fields = ['apply_project', 'apply_user', 'wish_deploy_time', 'conf_amend_explain', 'remark_explain']


DeployItemFormSet = inlineformset_factory(DeployApply, DeployItem, fields=('deploy_order_by', 'jenkins_version',
                                                                           'deploy_application', 'type'), extra=1,
                                          can_delete=True)
