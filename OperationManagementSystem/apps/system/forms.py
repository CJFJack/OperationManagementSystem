# -*- coding: utf-8 -*-

from django import forms
from OperationManagementSystem.apps.system.models import Application


class ApplicationForm(forms.ModelForm):
    fullname = forms.CharField(required=True, max_length=50)

    class Meta:
        model = Application
        exclude = ['ECS_lists', 'modified_user', 'modified_time', 'application_race']
