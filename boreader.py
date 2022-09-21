#!env python3
import argparse
import datetime
import sys
import os.path
import pyttsx3
import asyncio
import re
import configparser

def to_shorthand(text):
    final_text = text.lower()
    
    shorthand = {
        # Terran
        "supply depot": "depot",
        #"barracks": "rax",
        #"command center": "CC",
        "engineering bay": "E bay",
        "planetary fortress": "planetary",
        "missile turret": "turret",
        #"siege tank": "tank",
        #"widow mine": "mine",
        "orbital command": "orbital",
        "hyperflight rotors": "banshee speed",
        "rapid reignition system": "medivac speed",
        "advanced ballistics": "liberator range",
        "mag-field accelerator": "mag-field",
        "cloaking field": "banshee cloak",
        "personal cloaking": "ghost cloak",
        "weapon refit": "yamato",
        #"stimpack": "stim",
        "infernal pre-igniter": "blue flame",
        #"neosteel armor": "building armor",
        #"hi-sec auto tracking": "building range",
        "terran infantry armor level 1": "+1 infantry armor",
        "terran infantry weapons level 1": "+1 infantry attack",
        "terran infantry armor level 2": "+2 infantry armor",
        "terran infantry weapons level 2": "+2 infantry attack",
        "terran infantry armor level 3": "+3 infantry armor",
        "terran infantry weapons level 3": "+3 infantry attack",
        "terran ship weapons level 1": "+1 air attack",
        "terran ship weapons level 2": "+2 air attack",
        "terran ship weapons level 3": "+3 air attack",
        "terran vehicle weapons level 1": "+1 mek attack",
        "terran vehicle weapons level 2": "+2 mek attack",
        "terran vehicle weapons level 3": "+3 mek attack",
        "terran vehicle and ship armor level 1": "+1 mek armor",
        "terran vehicle and ship armor level 2": "+2 mek armor",
        "terran vehicle and ship armor level 3": "+3 mek armor",

        
        # Zerg
        "zergling": "ling",
        "hydralisk": "hydra",
        "mutalisk": "muta",
        "baneling": "bane",
        "hatchery": "hatch",
        "spawning pool": "pool",
        "evolution chamber": "evo chamber",
        "spine crawler": "spine",
        "spore crawler": "spore",
        "glial reconstitution": "roach speed",
        "muscular augments": "hydra speed",
        "metabolic boost": "zergling speed",
        "anabolic synthesis": "ultralisk speed",
        "centrifugal hooks": "baneling speed",
        "pneumatized carapace": "overlord speed",
        "grooved spines": "hydralisk range",
        "seismic spines": "lurker range",

        # Protoss
        "photon cannon": "cannon",
        "cybernetics core": "cyber core",
        "robotics facility": "robo",
        "robotics bay": "robo bay",
        "warp prism": "prism",
        "gravitic boosters": "observer speed",
        "flux vanes": "void ray speed",
        "resonating glaives": "glaives",
        "gravitic drive": "prism speed",
        "anion pluse-crystals": "phoenix range",
        "extended thermal lance": "thermal lance",
        "psionic storm": "psi storm",
        "shadow stride": "DT blink"
    }
    
    for word in shorthand:
        if word in final_text:
            final_text = final_text.replace(word, shorthand[word])
    
    return final_text

parser = argparse.ArgumentParser(description="Read out a SC2 build order.")
parser.add_argument('build', type=str, help='filename of the build to read in the builds folder')
parser.add_argument('--real', action='store_true', help='if true, dont apply the 1.02 scaling factor')
parser.add_argument('--scaling', type=float, default=1., help='speed scaling factor')
parser.add_argument('--speed', type=str, default='fastest', help='game speed')
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

if not os.path.isfile(args.build):
    args.build = "/home/tone/sc2/builds/" + args.build

with open(args.build, 'r') as build_order:
    countdown = 3 if args.real else 5;

    scaling = 1.
    match args.speed:
        case 'faster':
            scaling = 1.4 / 1.2
        case 'normal':
            scaling = 1.4
        case 'slow':
            scaling = 1.4 / 0.8
        case 'slower':
            scaling = 1.4 / 0.6
        case _:
            pass
    if args.scaling != 1.:
        scaling = 1/args.scaling
    if not args.real:
        scaling *= 1.02

    event_loop = asyncio.new_event_loop()
    starttime = event_loop.time()
    actual_start = starttime + countdown + 1

    for i in range(0, countdown):
        event_loop.call_at(starttime + i, perform_action, countdown-i, countdown-i)

    fast_forward = datetime.timedelta(minutes=int(args.time.split(":")[0]), seconds=int(args.time.split(":")[1]))
    for row in build_order.read().splitlines():
        if len(row) == 0 or row[0] == '#':
            continue
        # Formatting
        row = row.split(None, 1)
        actions = row[1]

        if args.shorthand:
            actions = to_shorthand(actions)

        clock = datetime.timedelta(minutes=int(row[0].split(":")[0]), seconds=int(row[0].split(":")[1]))
        if clock >= fast_forward:
            event_loop.call_at(actual_start + (clock.total_seconds() - fast_forward.total_seconds()) * scaling, perform_action, row, actions)

    event_loop.run_forever()
