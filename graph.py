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
        timing = s[1]

        if s[0] in keyAndTimes.keys():
            keyAndTimes[s[0]].append((timing, s[2]))
        else:
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
    parser.add_argument("samples", nargs="+")

    args = vars(parser.parse_args())

    fig, axs = plt.subplots(len(args["samples"]), 1)
    for n, sample_name in enumerate(args["samples"]):
        with open(sample_name, "r") as fin:
            sample = fromJson(fin)

        sortedKeyEvents = loadToLists(sample["events"], sample["starttime"])

        print("sample:{}".format(sample_name))
        for key in sortedKeyEvents.keys():
            x = [int(x[0]) for x in sortedKeyEvents[key]]
            y = [int(y[1]) for y in sortedKeyEvents[key]]
            print(key)
            print(x)
            print(y)
            axs[n].plot(x, y, label=key)

        fig.legend(title="keys")

    plt.show()
