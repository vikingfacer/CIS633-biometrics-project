#!/usr/bin/env python3

import argparse
import json
import statistics
import os


import eventCapture


def key_latency(data, hold_or_release):
    """
    Distance between key presses
    """
    hold = 0
    if hold_or_release:
        hold = 1

    presses = []
    for event in data["events"]:
        event[0] = event[0].strip("'\"")
        if int(event[2]) == hold:
            presses.append(event[1])
    presses = sorted(presses)

    pairs = []
    for i, press in enumerate(presses):
        if i + 1 < len(presses):
            pairs.append((press, presses[i + 1]))

    diffs = []
    for pair in pairs:
        delta = pair[1] - pair[0]
        diffs.append(delta)

    return {
        "average": statistics.mean(diffs),
        "median": statistics.median(diffs),
        "range": max(diffs) - min(diffs),
    }


def make_pairs(presses):
    sorted_presses = sorted(presses, key=lambda x: x[0])
    pairs = []
    for i, x in enumerate(sorted_presses):
        if i + 1 < len(sorted_presses):
            if int(x[1]) == 1 and int(sorted_presses[i + 1][1]) == 0:
                pairs.append((x, sorted_presses[i + 1]))
    return pairs


def key_hold(data):
    """
    Time of key held down
    """

    # all key events
    byKey = {}
    for event in data["events"]:
        event[0] = event[0].strip("'\"")

        # add key event to dictionary
        if str(event[0]).isalnum():
            if event[0] in byKey.keys():
                byKey[event[0]].append((event[1], event[2]))
            else:
                byKey[event[0]] = [(event[1], event[2])]
    pairs = []
    for keypress in byKey.values():
        pairs.extend(make_pairs(keypress))

    diffs = []
    for pair in pairs:
        delta = pair[1][0] - pair[0][0]
        diffs.append(delta)

    return {
        "average": statistics.mean(diffs),
        "median": statistics.median(diffs),
        "range": max(diffs) - min(diffs),
    }


def backtracking(data):
    """
    Count of backtracking (backspace)
    """
    return len(
        [x for x in data["events"] if (x[0] == "Key.backspace") and (int(x[2]) == 1)]
    )


def extract_features(files, outfilename):
    data = []
    for file in files:
        with open(file, "r") as fin:
            sample = json.load(fin)
            data.append(
                {
                    backtracking.__name__: backtracking(sample),
                    key_hold.__name__: key_hold(sample),
                    "hold_{}".format(key_latency.__name__): key_latency(sample, True),
                    "press_{}".format(key_latency.__name__): key_latency(sample, False),
                }
            )

        with open(outfilename, "w") as fout:
            fout.write(json.dumps(data))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="extract Features",
        description="""
        """,
    )
    parser.add_argument(
        "rawData",
    )
    parser.add_argument("--user")

    args = vars(parser.parse_args())
    list_of_files = []
    if os.path.isdir(args["rawData"]):
        list_of_files = [args["rawData"] + x for x in os.listdir(args["rawData"])]
    else:
        list_of_files = [args["rawData"]]

    extract_features(list_of_files, "{}_data.json".format(args["user"]))
