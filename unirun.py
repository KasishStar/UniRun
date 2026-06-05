#!/usr/bin/env python3

import sys
import os

from runtimes import xdg
from core.doctor import doctor
from core.detector import detect
from core.search import find_file
from core.history import add_entry, show_history
from core.install import install_package
from core.search_command import search_files

from runtimes import wine
from runtimes import waydroid
from runtimes import appimage
from runtimes import native

VERSION = "0.3"


def show_help():
    print(f"""
UniRun v{VERSION}

Commands:

run <file>
doctor
version
help

Examples:

unirun setup.exe
unirun game.apk
unirun xyz.AppImage
unirun search File (Searches any file in the system)
unirun install <package> (Installs a package)

unirun doctor
""")

def show_version():
    print(f"UniRun v{VERSION}")


def run_file(filepath):

    if (
        not filepath.startswith("http://")
        and not filepath.startswith("https://")
        and not os.path.exists(filepath)
    ):

        found = find_file(filepath)

        if found:

            print(f"[UniRun] Found: {found}")

            filepath = found

        else:

            print(f"[UniRun] File not found: {filepath}")
            return

    add_entry(filepath)
    runtime = detect(filepath)

    print(f"[UniRun] Detected runtime: {runtime}")

    if runtime == "windows":
        wine.launch(filepath)

    elif runtime == "android":
        waydroid.launch(filepath)

    elif runtime == "appimage":
        appimage.launch(filepath)

    elif runtime == "xdg":
        xdg.launch(filepath)

    elif runtime == "web":
        xdg.launch(filepath)

    else:
        native.launch(filepath)


def main():

    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1]

    known_commands = [
        "help",
        "version",
        "doctor",
        "history",
        "search",
        "install",
        "run"
    ]

    # Direct launch support
    if command not in known_commands:
        run_file(command)
        return

    if command == "help":
        show_help()

    elif command == "version":
        show_version()

    elif command == "doctor":
        doctor()

    elif command == "history":
        show_history()
    
    elif command == "search":

        if len(sys.argv) < 3:
            print("[UniRun] Missing search query")
            return

        search_files(sys.argv[2])

    elif command == "install":

        if len(sys.argv) < 3:
            print("[UniRun] Missing package name")
            return

        install_package(sys.argv[2])

    elif command == "run":

        if len(sys.argv) < 3:
            print("[UniRun] Missing file")
            return

        run_file(sys.argv[2])

    else:
        print("[UniRun] Unknown command")


if __name__ == "__main__":
    main()