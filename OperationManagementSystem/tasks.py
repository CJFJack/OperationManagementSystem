# -*- encoding: utf-8 -*-

from celery import Celery
from jenkinsapi.jenkins import Jenkins
from jenkinsapi.utils.crumb_requester import CrumbRequester

app = Celery('tasks',
             broker='redis://192.168.88.120:6379/0',
             backend='redis://192.168.88.120:6379/0')


@app.task(ignore_result=True)
def jenkins_build():
    jenkins_url = 'http://127.0.0.1:8080/'
    username = 'admin'
    password = 'Python@123'
    jenkins = Jenkins(jenkins_url, username=username, password=password,
                      requester=CrumbRequester(
                          baseurl=jenkins_url,
                          username=username,
                          password=password,
                      ))

    params = {'min': '3'}

    job = jenkins['test-job']
    qi = job.invoke(build_params=params)

    if qi.is_queued() or qi.is_running():
        qi.block_until_complete()

    build = qi.get_build()
    print build
    print build.get_console()
    print build._data['result']
