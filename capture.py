#!/usr/bin/env python3

"""
Capture is a program to capture keyboard events
for dynamic keystroke  authentication
"""

# std libs
from time import clock_gettime_ns, CLOCK_MONOTONIC

# imported libs
import attrs
import numpy
from pynput import keyboard

# custom libs
from eventCapture import keyState, eventCapture_ms


class Capturer:
    events = []
    startTime_ms = 0

    def __init__(self):
        self.events = []
        startTime_ms = self.time_ms()

    def time_ms(self):
        return clock_gettime_ns(CLOCK_MONOTONIC) / 1000

    def on_press(self, key):
        self.events.append(eventCapture_ms(key, self.time_ms(), keyState.PRESS))
        try:
            print("alphanumeric key {0} pressed".format(key.char))
        except AttributeError:
            print("special key {0} pressed".format(key))

    def on_release(self, key):
        self.events.append(eventCapture_ms(key, self.time_ms(), keyState.RELEASE))
        print("{0} released".format(key))
        if key == keyboard.Key.esc:
            # Stop listener
            return False


if "__main__" == __name__:
    cap = Capturer()
    # Collect events until released
    # with keyboard.Listener(on_press=cap.on_press, on_release=cap.on_release) as listener:
    #    listener.join()

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

    for e in cap.events:
        print(e)
