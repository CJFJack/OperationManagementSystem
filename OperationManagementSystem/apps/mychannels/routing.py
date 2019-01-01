# -*- coding: utf-8 -*-
from channels.routing import route
from OperationManagementSystem.apps.mychannels.consumers import *

channel_routing = [
    route("websocket.connect", ws_add),
    route("ws_message", ws_message),
    route("websocket.disconnect", ws_disconnect),

    route("ws_jenkins_connect", ws_jenkins_connect, path='^ws/jenkins/$'),
    route("ws_jenkins_build", ws_jenkins_build, path='^ws/jenkins/$'),
    route("ws_jenkins_disconnect", ws_jenkins_disconnect, path='^ws/jenkins/$'),
]
