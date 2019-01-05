# -*- encoding: utf-8 -*-

from jenkinsapi.jenkins import Jenkins
from jenkinsapi.utils.crumb_requester import CrumbRequester
from channels import Channel
from OperationManagementSystem.apps.jenkins.models import JenkinsJobList, JenkinsBuildHistory
import datetime


def jenkins_build(job_id, params=None):
    jenkins_url = 'http://localjenkins:8080/'
    username = 'admin'
    password = 'Python@123'
    job_obj = JenkinsJobList.objects.get(pk=job_id)
    job_obj.status = 1
    job_obj.save()
    try:
        jenkins = Jenkins(jenkins_url, username=username, password=password,
                          requester=CrumbRequester(
                              baseurl=jenkins_url,
                              username=username,
                              password=password,
                          ))
        try:
            job = jenkins[job_obj.name]
        except:
            job_obj.status = 2
            job_obj.save()
            return {'success': False, 'msg': 'jenkinsJobDoesNotExist：' + str(job_obj.name) + '，请先同步任务列表！'}
        start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if params is not None:
            qi = job.invoke(build_params=params)
        else:
            qi = job.invoke()

        if qi.is_queued() or qi.is_running():
            qi.block_until_complete()

        build = qi.get_build()
    except Exception as e:
        job_obj.status = 2
        job_obj.save()
        return {'success': False, 'msg': str(e)}
    else:
        if build._data['result'] == 'SUCCESS':
            job_obj.status = 2
            job_obj.save()
            JenkinsBuildHistory.objects.create(build_no=build.buildno, build_start_time=start_time, result=1, job=job_obj)
            msg = {'group': 'jenkins', 'result': 'SUCCESS', 'job_id': job_id,
                   'last_success_time': job_obj.get_last_success_build_time(),
                   'last_failure_time': job_obj.get_last_failure_build_time()}
            Channel("ws_jenkins_build").send(msg)
            return {'success': True, 'msg': ''}
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
            return {'success': True, 'msg': ''}