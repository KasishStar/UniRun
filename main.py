#!/usr/bin/env python3

import sys

from core.detector import detect

from runtimes import wine
from runtimes import waydroid
from runtimes import appimage
from runtimes import native


VERSION = "0.1"


def show_help():
    print("""
UniRun 0.1

Usage:

python main.py run <file>

Examples:

python main.py run setup.exe
python main.py run game.apk
python main.py run Blender.AppImage
""")


def run_file(filepath):
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

    elif command == "run":

        if len(sys.argv) < 3:
            print("Missing file")
            return

        filepath = sys.argv[2]

        run_file(filepath)

    else:
        print("Unknown command")


if __name__ == "__main__":
    main()