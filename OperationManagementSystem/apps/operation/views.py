# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from OperationManagementSystem.apps.operation.models import Release
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from django.core.files import File

import json
import os


@login_required(login_url='/login/')
@csrf_exempt
def config_deploy(request, release_id):
    """实例化"""
    r = Release.objects.get(pk=release_id)
    '''获取发布配置文件存放目录'''
    deploy_dir_path = settings.DEPLOY_DIR_PATH
    '''生成配置文件'''
    ecs = r.ECS.name
    config_path = os.path.join(deploy_dir_path, r.application.fullname, ecs, 'release_config')
    if not os.path.exists(config_path):
        os.makedirs(config_path)
    for c in r.application.configfile_set.all():
        if c.filename:
            file_name = os.path.join(config_path, c.filename)
            with open(file_name, 'w') as f:
                config_file = File(f)
                config_file.write(str(c.content))
        else:
            return HttpResponse(json.dumps({'success': False}), content_type="application/json")
    """更新Release表信息"""
    r.status = 'Y'
    r.modified_user = request.user.username
    r.save()
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")
