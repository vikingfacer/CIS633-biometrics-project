#!/usr/bin/env python3

"""
Capture is a program to capture keyboard events
for dynamic keystroke  authentication
"""

# std libs
import argparse
import contextlib
import time
from datetime import datetime
import json
import re
import os

# imported libs
from pynput import keyboard

# custom libs
from eventCapture import keyState, eventCapture_ms, eventEncoder
from extract_features import extract_features
from verify import getAvgMedRng, verify, graph_stats


@contextlib.contextmanager
def pushd(new_dir):
    previous_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(previous_dir)


class Capturer:
    events = []
    startTime_ms = 0

    def __init__(self, capname):
        self.capname = capname
        self.events = []
        self.startTime_ns = None

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

        if self.startTime_ns != None:
            self.events.append(
                eventCapture_ms(str(key), self.delta_time_ms(), keyState.PRESS)
            )
        else:
            self.startTime_ns = time.monotonic_ns()
            self.events.append(eventCapture_ms(str(key), 0, keyState.PRESS))

    def on_release(self, key):

        if self.startTime_ns != None:
            self.events.append(
                eventCapture_ms(str(key), self.delta_time_ms(), keyState.RELEASE)
            )
        if key == keyboard.Key.esc:
            # Stop listener
            return False


def procedure(name, prompt, N):
    datafiles = []
    for x in range(0, N):
        if x > 0:
            datafiles.append(get_sample(name, prompt + " Again: ", x))
        else:
            datafiles.append(get_sample(name, prompt, x))
    return datafiles


def get_sample(name, prompt, i):
    cap = Capturer("{}_{}.json".format(name, i))
    listener = keyboard.Listener(on_press=cap.on_press, on_release=cap.on_release)
    listener.start()
    password_new = input(prompt)
    listener.stop()
    cap.write_sample()
    return cap.capname


def collection_setup(username, capture_procedure, prompt, N):

    sample_dir = os.path.join(os.getcwd(), username)
    if not os.path.exists(sample_dir):
        os.mkdir(sample_dir)

    with pushd(sample_dir):
        return capture_procedure(username, "Enter " + prompt + "\n", N)


def verifyAgainstAll(CompareStat, threshold):
    for k in CompareStat.keys():
        print("with {}: ".format(k))
        if verify(CompareStat[k][0], CompareStat[k][0], threshold):
            print("User is Verified")
        else:
            print("User Not Verified")


if "__main__" == __name__:

    parser = argparse.ArgumentParser(
        prog="Capturer",
        description="""
        Program to collect keystroke samples.
        User types in username
        Then types in password x5
        """,
    )

    parser.add_argument("-p", "--prompt", default="Template Text", type=str)
    parser.add_argument("-v", "--verify", default=False, action="store_true")
    parser.add_argument("-g", "--graph", default=False, action="store_true")
    parser.add_argument("--user", default=None)
    parser.add_argument("-t", "--threshold", default=2, type=float)
    args = vars(parser.parse_args())

    if args["user"] == None:
        username = input("Input User Name: ")
        time.sleep(0.5)
    else:
        username = args["user"]

    if args["verify"]:
        sample_dir = os.path.join(os.getcwd(), username)

        # Get template_data
        with pushd(sample_dir):
            with open("{}_data.json".format(username)) as f:
                template = json.load(f)

        # Get verification entry
        list_of_data = [
            collection_setup(username, get_sample, args["prompt"], "verify")
        ]

        # Extract verification entry features
        with pushd(sample_dir):
            verify_features = extract_features(
                list_of_data, "{}_verify_data.json".format(username)
            )

        # Get feature Stats of template & verification text
        means, medians, ranges = getAvgMedRng(template)
        v_means, v_medians, v_ranges = getAvgMedRng(verify_features)

        stats = {
            "mean": [means, v_means],
            "median": [medians, v_medians],
            "range": [ranges, v_ranges],
        }
        # Verify
        verifyAgainstAll(
            stats,
            args["threshold"],
        )

        # Graph
        if args["graph"] == True:
            graph_stats(stats)
    else:
        # collect template data
        sample_dir = os.path.join(os.getcwd(), username)
        list_of_data = collection_setup(username, procedure, args["prompt"], 5)

        # Extract features from template data
        with pushd(sample_dir):
            extracted = extract_features(list_of_data, "{}_data.json".format(username))
            means, medians, ranges = getAvgMedRng(extracted)
