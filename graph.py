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
    parser.add_argument("-t", "--type", default="sample")
    parser.add_argument("-x")
    parser.add_argument("-y")

    args = vars(parser.parse_args())

    if args["type"] == "sample":
        fig, axs = plt.subplots(len(args["samples"]), 1)
        if len(args["samples"]) == 1:
            axs = [axs]
        for n, ax in enumerate(axs):
            with open(args["samples"][n], "r") as fin:
                sample = fromJson(fin)

            sortedKeyEvents = loadToLists(sample["events"], sample["starttime"])

            print("sample:{}".format(args["samples"][n]))
            for key in sortedKeyEvents.keys():
                x = [int(x[0]) for x in sortedKeyEvents[key]]
                y = [int(y[1]) for y in sortedKeyEvents[key]]
                print(key)
                print(x)
                print(y)
                ax.plot(x, y, label=key)

            fig.legend(title="keys")
    elif args["type"] == "scatter":
        plt.scatter(x, y)
    plt.show()
