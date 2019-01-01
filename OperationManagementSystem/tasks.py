# -*- encoding: utf-8 -*-

from celery import Celery
from jenkinsapi.jenkins import Jenkins
from jenkinsapi.utils.crumb_requester import CrumbRequester
from channels import Channel
from OperationManagementSystem.apps.jenkins.models import JenkinsJobList, JenkinsBuildHistory
import celeryconfig
import datetime

app = Celery()
app.config_from_object(celeryconfig)


# @app.task()
def jenkins_build(job_name, job_id):
    jenkins_url = 'http://192.168.88.102:8080/'
    username = 'admin'
    password = 'Python@123'
    job_obj = JenkinsJobList.objects.get(pk=job_id)
    try:
        jenkins = Jenkins(jenkins_url, username=username, password=password,
                          requester=CrumbRequester(
                              baseurl=jenkins_url,
                              username=username,
                              password=password,
                          ))

        params = {'min': 1}

        job = jenkins[job_name]
        qi = job.invoke(build_params=params)

        if qi.is_queued() or qi.is_running():
            qi.block_until_complete()

        build = qi.get_build()
    except Exception as e:
        job_obj.status = 2
        job_obj.save()
        return (False, e)
    else:
        start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if build._data['result'] == 'SUCCESS':
            job_obj.status = 2
            job_obj.save()
            JenkinsBuildHistory.objects.create(build_no=build.buildno, build_start_time=start_time, result=1, job=job_obj)
            msg = {'group': 'jenkins', 'result': 'SUCCESS', 'job_id': job_id,
                   'last_success_time': job_obj.get_last_success_build_time(),
                   'last_failure_time': job_obj.get_last_failure_build_time()}
            Channel("ws_jenkins_build").send(msg)
        if build._data['result'] == 'FAILURE':
            job_obj.status = 2
            job_obj.save()
            try:
                JenkinsBuildHistory.objects.create(build_no=build.buildno, build_start_time=start_time, result=0,
                                                   console=build.get_console().decode('utf-8'), job=job_obj)
            except:
                JenkinsBuildHistory.objects.create(build_no=build.buildno, build_start_time=start_time, result=0,
                                                   console=build.get_console().decode('gbk'), job=job_obj)
            msg = {'group': 'jenkins', 'result': 'FAILURE', 'job_id': job_id,
                   'last_success_time': job_obj.get_last_success_build_time(),
                   'last_failure_time': job_obj.get_last_failure_build_time()}
            Channel("ws_jenkins_build").send(msg)
            return (True, '')
