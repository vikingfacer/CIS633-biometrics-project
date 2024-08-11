#!/usr/bin/env python3

"""
Capture is a program to capture keyboard events
for dynamic keystroke  authentication
"""

# std libs
import argparse
from time import clock_gettime_ns, CLOCK_MONOTONIC
from datetime import datetime
import json

# imported libs
from pynput import keyboard

# custom libs
from eventCapture import keyState, eventCapture_ms, eventEncoder


class Capturer:
    events = []
    startTime_ms = 0

    def __init__(self):
        self.events = []
        startTime_ms = 0

    def time_ms(self):
        return clock_gettime_ns(CLOCK_MONOTONIC) / 1000

    def on_press(self, key):
        if self.startTime_ms == 0:
            self.startTime_ms = self.time_ms()

        self.events.append(eventCapture_ms(str(key), self.time_ms(), keyState.PRESS))
        try:
            print("alphanumeric key {0} pressed".format(key.char))
        except AttributeError:
            print("special key {0} pressed".format(key))

    def on_release(self, key):
        self.events.append(eventCapture_ms(str(key), self.time_ms(), keyState.RELEASE))
        print("{0} released".format(key))
        if key == keyboard.Key.esc:
            # Stop listener
            return False


def procedure(cap):
    # ...or, in a non-blocking fashion:
    listener = keyboard.Listener(on_press=cap.on_press, on_release=cap.on_release)
    listener.start()

    # register user
    username = input("Input User Name: ")
    # enter password 5 times
    password = None
    prompt = "Input password {}/{}"
    samples = 5
    i = 0
    while i < samples:
        password_new = input(prompt.format(i, samples))
        if password == None:
            password = password_new
        elif password_new == password:
            print("Passwords matched!")
            i += 1
        else:
            print("Passwords did not match please retry...")

    return username


if "__main__" == __name__:

    parser = argparse.ArgumentParser(
        prog="Capturer",
        description="""
        Program to collect keystroke samples.
        User types in username
        Then types in password x5
        """,
    )
    parser.add_argument("-o", "--output")

    args = vars(parser.parse_args())

    cap = Capturer()

    username = procedure(cap)

    if args["output"] == None:
        capname = "{}-{}.json".format(
            username, datetime.now().strftime("%m%d%y-%H%M%S")
        )
    else:
        capname = args["output"]

    with open(capname, "w") as file_cap:
        json.dump(
            {"starttime": cap.startTime_ms, "events": cap.events},
            file_cap,
            cls=eventEncoder,
        )

    for e in cap.events:
        print(e)
