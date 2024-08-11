#!/usr/bin/env python3

"""
event Capture:
    namedtuple to represent Keyboard events in time
"""

from collections import namedtuple
from enum import Enum
import json


class keyState(Enum):
    RELEASE = 0
    PRESS = 1


eventCapture_ms = namedtuple("eventCapturems", ["key", "time", "trigger"])


class eventEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, eventCapture_ms):
            return "{key: {}, time: {}, trigger: {}}".format(
                str(o.key).replace("Key.", ""),
                str(o.time),
                eventEncoder(self, o.trigger),
            )
        elif isinstance(o, keyState):
            return "{}".format(o.value)

        return eventEncoder(self, o)
