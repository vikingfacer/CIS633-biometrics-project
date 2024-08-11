#!/usr/bin/env python3

# std libs
import argparse
import json

# imported libs
import matplotlib.pyplot as plt

# custom libs
from eventCapture import eventCapture_ms, eventEncoder, keyState


def fromJson(file):
    return json.load(file)


def loadToLists(events, starttime):
    """
    {
        'key' : [ (<0 or 1>, <time in ms>), ]
        ...
    }
    """
    keyAndTimes = {}
    for s in events:
        if s[0] in keyAndTimes.keys():
            keyAndTimes[s[0]].append((s[1] - starttime, s[2]))
        else:
            timing = s[1] - starttime
            keyAndTimes[s[0]] = [(timing, s[2])]

    return keyAndTimes


if "__main__" == __name__:
    parser = argparse.ArgumentParser(
        prog="graph",
        description="""
        Program to visualize keystroke samples.
        Input: json of samples
        Show Graph
        """,
    )
    parser.add_argument("samples")

    args = vars(parser.parse_args())

    with open(args["samples"], "r") as fin:
        samples = fromJson(fin)

    sortedKeyEvents = loadToLists(samples["events"], samples["starttime"])

    step = 0
    for key in sortedKeyEvents.keys():
        x = [int(x[0]) for x in sortedKeyEvents[key]]
        y = [int(y[1]) + step for y in sortedKeyEvents[key]]
        plt.step(x, y, label=key)
        step += 2

    plt.legend(title="keys")

    plt.show()
