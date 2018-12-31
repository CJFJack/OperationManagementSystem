# -*- coding: utf-8 -*-

CELERY_TIMEZONE = 'Asia/Shanghai'


BROKER_URL = 'redis://192.168.88.120:6379/0'
CELERY_IMPORTS = ('tasks', )

CELERY_RESULT_BACKEND = 'amqp'
CELERY_RESULT_PERSISTENT = True
CELERY_TASK_RESULT_EXPIRES = None

CELERY_DEFAULT_QUEUE = 'default'
CELERY_QUEUES = {
    'default': {
        'binding_key': 'task.#',
    },
    'jenkins_build': {
        'binding_key': 'jenkins_build.#',
    },
}
CELERY_DEFAULT_EXCHANGE = 'tasks'
CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
CELERY_DEFAULT_ROUTING_KEY = 'task.default'
CELERY_ROUTES = {
    'tasks.jenkins_build': {
        'queue': 'jenkins_build',
        'routing_key': 'jenkins_build.a_jenkins_build'
    },
}
