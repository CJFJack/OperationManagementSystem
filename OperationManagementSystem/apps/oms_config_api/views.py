# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User


# API example
class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    调用方法：
    - curl
        curl -X GET http://<your project url>/oms_config_api/list_users/ -H 'Authorization: Token <your token>'
    - Python Script
        安装 requests 库：pip install requests
        example:
            # -*- coding: utf-8 -*-

            import requests

            url = 'http://<your project url>/oms_config_api/list_users/'
            headers = {
                 'Accept': 'application/json',
                 'Authorization': 'Token <your token>',
            }

            r = requests.get(url, headers=headers, timeout=15, verify=False)
            print r.json()

    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)
