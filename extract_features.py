#!/usr/bin/env python3

import argparse
import json

import eventCapture


def key_hold_latency(data):
    """
    Distance between key presses
    """
    pass


def key_hold(data):
    """
    Time of key held down
    """
    pass


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
    pass
