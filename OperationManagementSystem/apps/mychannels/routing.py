# -*- coding: utf-8 -*-
from channels.routing import route
from OperationManagementSystem.apps.mychannels.consumers import ws_add, ws_message, ws_disconnect

channel_routing = [
    route("websocket.connect", ws_add),
    route("ws_message", ws_message),
    route("websocket.disconnect", ws_disconnect),
]