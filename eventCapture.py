#!/usr/bin/env python3

"""
event Capture:
    namedtuple to represent Keyboard events in time
"""

from collections import namedtuple
from enum import Enum


class keyState(Enum):
    RELEASE = 0
    PRESS = 1


eventCapture_ms = namedtuple("eventCapturems", ["key", "time", "trigger"])
