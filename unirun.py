#!/usr/bin/env python3

import sys
import os
import shutil

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
======================================================================
  UniRun v{VERSION} - "Run Anything. Anywhere."
======================================================================
UniRun is a universal application orchestration layer that automatically 
detects, configures, and matches binaries to their correct runtimes.

USAGE:
    unirun <command> [arguments]
    unirun <file_path_or_command_name>

CORE COMMANDS:
    run <file>          Explicitly run a targeted application file.
    search <query>      Fuzzy search for matching files across the filesystem.
    install <runtime>   Automatically install missing compatibility layers.
    doctor              Check the status of system compatibility backends.
    history             View the execution log of previously launched files.
    version             Display current software release variant.
    help                Show this interactive command registry.

AUTOMATIC EXECUTION (Direct Launch):
    You can completely omit the "run" command. Simply passing a file name, 
    path, or global application token will cause UniRun to intercept it,
    evaluate the dependency platform, and execute it instantly.

EXAMPLES:
    unirun setup.exe                    -> Instantly provisions via Wine
    unirun mobile_game.apk              -> Hands off execution to Waydroid
    unirun application.AppImage         -> Mounts and executes standalone image
    unirun firefox                      -> Seamlessly launches system native binaries
    unirun search minecraft             -> Locates asset files across partitions
    unirun install flatpak              -> Downloads package manager dependency

======================================================================
""")

def show_version():
    print(f"UniRun Universal Layer - v{VERSION}")


def run_file(filepath):
    # 1. Handle remote web URLs directly
    if filepath.startswith("http://") or filepath.startswith("https://"):
        add_entry(filepath)
        print(f"\n[UniRun]  Remote target identified. Routing via Web Engine...")
        xdg.launch(filepath)
        return

    # 2. Check if it's NOT a direct path on your filesystem
    if not os.path.exists(filepath):
        # Check if it is a globally installed system CLI command/binary
        system_binary = shutil.which(filepath)
        if system_binary:
            filepath = system_binary
        else:
            # If it's not local or global, check using your fuzzy finder logic
            print(f"[UniRun] 🔍 Local file target not found. Initiating fuzzy filesystem lookup...")
            found = find_file(filepath)
            if found:
                print(f"[UniRun]  Target resolved: {found}")
                filepath = found
            else:
                print(f"[UniRun] ❌ Error: Specified file or command path token could not be resolved: '{filepath}'")
                return

    add_entry(filepath)
    runtime = detect(filepath)

    print(f"[UniRun] 🛠️  Analyzing binaries... Compatibility layer selected: [{runtime.upper()}]")

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
            print("[UniRun] ❌ Error: Missing search parameters. Syntax: unirun search <query>")
            return
        search_files(sys.argv[2])

    elif command == "install":
        if len(sys.argv) < 3:
            print("[UniRun] ❌ Error: Missing target name. Syntax: unirun install <package>")
            return
        install_package(sys.argv[2])

    elif command == "run":
        if len(sys.argv) < 3:
            print("[UniRun] ❌ Error: Missing targeted execution reference file path.")
            return
        run_file(sys.argv[2])

    else:
        print("[UniRun] ❌ Unknown command entered.")


if __name__ == "__main__":
    main()