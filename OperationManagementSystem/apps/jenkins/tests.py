# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
#
from jenkinsapi.jenkins import Jenkins
from jenkinsapi.utils.crumb_requester import CrumbRequester

jenkins_url = 'http://127.0.0.1:8080/'
username = 'admin'
password = 'Python@123'
jenkins = Jenkins(jenkins_url, username=username, password=password,
                  requester=CrumbRequester(
                      baseurl=jenkins_url,
                      username=username,
                      password=password,
                  ))
#
# params = {'min': 1}
#
# # This will start the job in non-blocking manner
# # jenkins.build_job('test-job', params)
#
#
# # This will start the job and will return a QueueItem object which
# # can be used to get build results
# job = jenkins['test-job']
# qi = job.invoke(build_params=params)
#
# # Block this script until build is finished
# if qi.is_queued() or qi.is_running():
#     qi.block_until_complete()
#
# build = qi.get_build()
# print build
# print build.get_console().decode('gbk')
# print build._data
# print build._data['result']

# import os
#
# os.environ['DJANGO_SETTINGS_MODULE'] = 'OperationManagementSystem.settings'
#
# import django
#
# django.setup()
# from OperationManagementSystem.tasks import jenkins_build
#
# print jenkins_build.delay(1)

jobName = jenkins.keys()[0]  # get the first job

config = jenkins[jobName].get_config()

print(jenkins.keys())
