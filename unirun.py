#!/usr/bin/env python3

import sys
import os

from core.doctor import doctor
from core.detector import detect

from runtimes import wine
from runtimes import waydroid
from runtimes import appimage
from runtimes import native

VERSION = "0.2"


def show_help():
    print(f"""
UniRun v{VERSION}

Commands:

run <file>
doctor
version
help

Examples:

python main.py run setup.exe
python main.py run game.apk
python main.py doctor
""")


def show_version():
    print(f"UniRun v{VERSION}")


def run_file(filepath):

    if not os.path.exists(filepath):
        print(f"[UniRun] File not found: {filepath}")
        return

    runtime = detect(filepath)

    print(f"[UniRun] Detected runtime: {runtime}")

    if runtime == "windows":
        wine.launch(filepath)

    elif runtime == "android":
        waydroid.launch(filepath)

    elif runtime == "appimage":
        appimage.launch(filepath)

    else:
        native.launch(filepath)


def main():

    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1]

    if command == "help":
        show_help()

    elif command == "version":
        show_version()

    elif command == "doctor":
        doctor()

    elif command == "run":

        if len(sys.argv) < 3:
            print("[UniRun] Missing file")
            return

        run_file(sys.argv[2])

    else:
        print("[UniRun] Unknown command")


if __name__ == "__main__":
    main()