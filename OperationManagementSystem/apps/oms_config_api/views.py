# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from OperationManagementSystem.apps.operation.models import Release
from django.conf import settings
from django.core.files import File
from django.http import HttpResponse
import json
import os
import logging
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


# API GET Example
class APIGetExample(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    调用方法：
    - curl
        curl -X GET http://<your project url>/oms_config_api/api_get_example/ -H 'Authorization: Token <your token>'
    - Python Script
        安装 requests 库：pip install requests
        example:
            # -*- coding: utf-8 -*-

            import requests

            url = 'http://<your project url>/oms_config_api/api_get_example/'
            headers = {
                'Accept': 'application/json',
                'Authorization': 'Token <your token>',
            }

            r = requests.get(url, headers=headers, timeout=15, verify=False)
            print(r.json())

    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)


# API POST Example
class APIPostExample(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    调用方法：
    - curl
        curl -X POST http://<your project url>/oms_config_api/api_post_example/ -H 'Authorization: Token <your token>'
    - Python Script
        安装 requests 库：pip install requests
        example:
            # -*- coding: utf-8 -*-

            import requests, json

            url = 'http://<your project url>/oms_config_api/api_post_example/'
            headers = {
                'Accept': 'application/json',
                'Authorization': 'Token <your token>',
            }
            post_data = {
                'data': 'Hello world!'
            }

            r = requests.post(url, headers=headers, data=post_data, timeout=15, verify=False)
            print r.json()

    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        """
        Return a list of all users.
        """
        p_data = request.POST
        return Response(p_data)


class DeployConfig(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        try:
            p_data = request.POST
            print p_data
            release_id = request.POST['release_id']
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
            return Response({'success': True})
        except Exception, e:
            logging.exception(e)
            return Response({'success': False})
