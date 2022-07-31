#!env python
import argparse
import datetime
import sc_bo_utils
import sys
import os.path
import pyttsx3
import asyncio

parser = argparse.ArgumentParser(description="Read out a SC2 build order.")
parser.add_argument('build', type=str, help='filename of the build to read in the builds folder')
parser.add_argument('--shorthand', type=bool, default=True, help='whether to use shorthand names for units and buildings')
parser.add_argument('--time', type=str, default="0:00", help='timestamp to forward to in-game')
args = parser.parse_args()

def perform_action(printed_statement, spoken_text):
    print(printed_statement)
    engine.say(spoken_text)
    engine.runAndWait()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', 'english+f4')
engine.setProperty('rate', 200)

with open(args.build, 'r') as build_order:
    event_loop = asyncio.new_event_loop()
    starttime = event_loop.time()
    actual_start = starttime + 6

    for i in range(0, 5):
        event_loop.call_at(starttime + i, perform_action, 5-i, 5-i)

    fast_forward = datetime.timedelta(minutes=int(args.time.split(":")[0]), seconds=int(args.time.split(":")[1]))
    for row in build_order.read().splitlines():
        if len(row) == 0 or row[0] == '#':
            continue
        # Formatting
        row = row.split(None, 1)
        actions = row[1]

        if args.shorthand:
            actions = sc_bo_utils.to_shorthand(actions)

        clock = datetime.timedelta(minutes=int(row[0].split(":")[0]), seconds=int(row[0].split(":")[1]))
        if clock >= fast_forward:
            event_loop.call_at(actual_start + (clock.total_seconds() - fast_forward.total_seconds()) * 1.02, perform_action, row, actions)

    event_loop.run_forever()
