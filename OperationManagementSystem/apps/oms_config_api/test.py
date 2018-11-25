# -*- coding: utf-8 -*-

import requests
from OperationManagementSystem.apps.config.models import Configfile

config_file_object = Configfile.objects.first()
config_file_content = config_file_object.content
url = 'http://127.0.0.1:8000/oms_config_api/deploy_config/'
headers = {
    'Accept': 'application/json',
    'Authorization': 'Token 0ca581d90e7d82155083c1018416ab5100c79621',
}
post_data = {
    'p_data': 'Hello world!',
    'config_file_content': config_file_content
}

r = requests.post(url, headers=headers, data=post_data, timeout=15, verify=False)
print r.json()

# curl -X GET http://127.0.0.1:8000/oms_config_api/api_get_example/ -H 'Authorization: Token <your token>'




