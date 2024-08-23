#!/usr/bin/env python3

"""
Capture is a program to capture keyboard events
for dynamic keystroke  authentication
"""

# std libs
import argparse
import time
from datetime import datetime
import json
import re

# imported libs
from pynput import keyboard

# custom libs
from eventCapture import keyState, eventCapture_ms, eventEncoder


class Capturer:
    events = []
    startTime_ms = 0

    def __init__(self, capname):
        self.capname = capname
        self.events = []
        self.startTime_ns = time.monotonic_ns()

    def write_sample(self):
        with open(self.capname, "w") as file_cap:
            json.dump(
                {"starttime": self.startTime_ms, "events": self.events},
                file_cap,
                cls=eventEncoder,
            )

    def delta_time_ms(self):
        return time.monotonic_ns() - self.startTime_ns

    def on_press(self, key):

        self.events.append(
            eventCapture_ms(str(key), self.delta_time_ms(), keyState.PRESS)
        )

    def on_release(self, key):
        self.events.append(
            eventCapture_ms(str(key), self.delta_time_ms(), keyState.RELEASE)
        )
        if key == keyboard.Key.esc:
            # Stop listener
            return False


def procedure():
    # ...or, in a non-blocking fashion:

    # register user
    sample_name = input("Input User Name: ")
    time.sleep(0.5)

    # enter password 5 times
    password = None
    prompt = "Enter text\n"
    for x in range(0, 5):
        cap = Capturer("{}_{}.json".format(sample_name, x))
        listener = keyboard.Listener(on_press=cap.on_press, on_release=cap.on_release)
        listener.start()
        password_new = input(prompt)
        listener.stop()
        cap.write_sample()


def validate_phrase(phrase):
    valid = False
    special_regex = re.compile("[@_!#$%^&*()<>?/\|}{~:]")
    if special_regex.search(phrase):
        valid = True
        return valid


if "__main__" == __name__:

    parser = argparse.ArgumentParser(
        prog="Capturer",
        description="""
        Program to collect keystroke samples.
        User types in username
        Then types in password x5
        """,
    )

    procedure()
