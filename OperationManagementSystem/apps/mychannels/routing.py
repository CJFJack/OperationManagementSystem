# -*- coding: utf-8 -*-
from channels.routing import route
from OperationManagementSystem.apps.mychannels.consumers import *

channel_routing = [
    route("websocket.connect", ws_add, path=r"^/mychannels/"),
    route("ws_message", ws_message),
    route("websocket.disconnect", ws_disconnect, path=r"^/mychannels/"),

    route("websocket.connect", ws_jenkins_connect, path=r"^/ws/jenkins/"),
    route("ws_jenkins_build", ws_jenkins_build),
    route("websocket.disconnect", ws_jenkins_disconnect, path=r"^/ws/jenkins/"),
]
