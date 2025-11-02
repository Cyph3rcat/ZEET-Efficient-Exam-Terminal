#!/usr/bin/env python3
"""
ZEET Core — Rich + pygame scaffold (single file)

Requirements:
  pip install rich prompt_toolkit pygame python-dotenv

Usage:
  - create ./sounds and drop optional switch.mp3 button.mp3 grade.mp3
  - python zeet.py
"""

import os
import sys
import time
import json
import threading
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional, Dict

# UI libs
from prompt_toolkit import Application
from prompt_toolkit.layout import Layout, HSplit, VSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.widgets import TextArea, Frame
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts import input_dialog, message_dialog

# import rich
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn

# essential data structures
from structures import QuestionState, Session

#import functions
import soundsfn # pygame sound functions
from animate import boot_sequence, splash_screen # animations
from render import start_menu, interactive_carousel # UI rendering and interaction

# directories
ROOT = Path.cwd() # current working directory typeshit
SESSIONS_DIR = ROOT / "sessions"
SESSIONS_DIR.mkdir(exist_ok=True)

# process config file #import styles, users, assign to variables
with open("config.json", "r") as f:
    config = json.load(f)
styleMenu = Style.from_dict(config["menu"])
styleCarousel = Style.from_dict(config["carousel"])
styleDialogue = Style.from_dict(config["dialogue"])
try:
    user = "@"+config["user"]["name"]
    print(user)
except :
    user = "@student"

selected = 0 #global selected for menu
console = Console() #initialize rich console

# Global settings
SETTINGS = {
    "sound": True,
    "editor": os.environ.get("EDITOR", "nano"),
}
soundsfn.set_enabled(SETTINGS["sound"])

# test if pygame ragequit
try: 
    PYGAME = True
    import pygame
except Exception:
    PYGAME = False
    print("Warning: pygame not available; sound disabled.", file=sys.stderr)

# ---------- Demo/sample questions (replace with generator later) ----------
SAMPLE = [
    QuestionState(1, "mcq", "What is the default HTTP port?", ["20", "21", "80", "443"], answer="2", points=1),
    QuestionState(2, "short", "Briefly describe the 3-way TCP handshake.", [], answer="SYN SYN-ACK ACK", points=4),
    QuestionState(3, "mcq", "IP is in which OSI layer?", ["App", "Transport", "Network", "Link"], answer="2", points=1),
    QuestionState(4, "essay", "Compare TCP and UDP (150-250 words).", [], answer=None, points=10),
]

# ---------- Menu UI ----------

menu_items = ["New Session", "Resume Session", "Settings", "Quit"]

# ---------- Settings UI ----------
def settings_menu():
    ans = input_dialog(title="Settings", text=f"Sound is {'ON' if SETTINGS['sound'] else 'OFF'}\nToggle sound? (y/n)").run()
    if ans and ans.lower().startswith("y"):
        SETTINGS["sound"] = not SETTINGS["sound"]
        soundsfn.set_enabled(SETTINGS["sound"])
        message_dialog(title="Settings", text=f"Sound is now {'ON' if SETTINGS['sound'] else 'OFF'}").run()

def toggle_sound():
    SETTINGS["sound"] = not SETTINGS["sound"]
    soundsfn.set_enabled(SETTINGS["sound"])

# ---------- Main ----------
def choose_resume():
    files = sorted(SESSIONS_DIR.glob("*.json"))
    if not files:
        message_dialog(title="Resume", text="No saved sessions found.").run()
        return None
    choices = "\n".join([f"{i+1}. {p.name}" for i, p in enumerate(files)])
    sel = input_dialog(title="Resume", text=f"Saved sessions:\n{choices}\n\nEnter number to resume:").run()
    try:
        idx = int(sel) - 1
        return Session.load(files[idx])
    except Exception:
        message_dialog(title="Resume", text="Invalid selection.").run()
        return None

#the code runs here lol
def main(): 

    # boot_sequence expects (duration, user)
    boot_sequence(3, user)

    # splash_screen expects the type_text as the first argument
    splash_screen(".ZEET//Efficient Exam Terminal")
    
    while True:
        selected_ref = [0]
        choice = start_menu(menu_items, styleMenu, SETTINGS, toggle_sound, selected_ref)
        if choice == "New Session":
            # load files in documents
            for file in Path.cwd().glob("documents/*"):
                console.print(f"Found document: {file.name}")
                # append to menu list for found documents
                # summon the menu to choose which file to extract (could we use start menu)
                # then break from the loop
            # run the extractor on the chosen file(given the right file type) to get the block file and create payload
            # call ai to generate questions from the payload, generate json sesh file


            subj = input_dialog(title="New Session", text="Subject name (or press Enter for demo):", style = styleDialogue).run() or f"session_{int(time.time())}"
            # TODO: ask for files / counts; for now use SAMPLE
            sess = Session(title=subj, questions=[QuestionState(**q.__dict__) for q in SAMPLE])
            interactive_carousel(sess)
        elif choice == "Resume Session":
            sess = choose_resume()
            if sess:
                interactive_carousel(sess)
        elif choice == "Settings":
            settings_menu()
        elif choice == "Quit":
            console.print("ZEET shutting down. glfyt ✨")
            break
        else:
            break

if __name__ == "__main__":
    try:
        # final sanity: if pygame isn't available, keep sound disabled
        if not PYGAME:
            SETTINGS["sound"] = False
        else:
            soundsfn.set_enabled(SETTINGS["sound"])
        main()
    except KeyboardInterrupt:
        console.print("\nInterrupted. Bye.")
    except SystemExit as e:
        console.print(str(e))
