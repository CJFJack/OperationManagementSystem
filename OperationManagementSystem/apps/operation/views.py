# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from OperationManagementSystem.apps.config.models import Configfile

import json
import requests


@login_required(login_url='/login/')
@csrf_exempt
def config_deploy(request, release_id):
    config_file_object = Configfile.objects.first()
    config_file_content = config_file_object.content
    url = 'http://127.0.0.1:8000/oms_config_api/deploy_config/'
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Token 0ca581d90e7d82155083c1018416ab5100c79621',
    }
    post_data = {
        'config_file_content': config_file_content,
        'release_id': release_id
    }
    try:
        r = requests.post(url, headers=headers, data=post_data, timeout=15, verify=False)
        if r.status_code == 200:
            return HttpResponse(json.dumps({'success': True}), content_type="application/json")
        else:
            msg = r.json()['detail']
            return HttpResponse(json.dumps({'success': False, 'msg': msg}), content_type="application/json")
    except Exception as e:
        return JsonResponse({'success': False, 'msg': str(e)})

