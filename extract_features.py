#!/usr/bin/env python3

import argparse
import json
import statistics

import eventCapture


def key_hold_latency(data):
    """
    Distance between key presses
    """

    presses = []
    for event in data["events"]:
        event[0] = event[0].strip("'\"")
        if int(event[2]) == 1:
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


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="extract Features",
        description="""
        """,
    )
    parser.add_argument(
        "samples",
    )

    args = vars(parser.parse_args())
    with open(args["samples"], "r") as fin:
        sample = json.load(fin)
    print(sample)
    print(backtracking(sample))
    print(key_hold(sample))
    print(key_hold_latency(sample))
    pass
