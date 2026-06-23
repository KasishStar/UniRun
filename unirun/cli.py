import sys
import os
import shutil
import argparse

from unirun import VERSION
from unirun.runtimes import xdg
from unirun.core.doctor import doctor
from unirun.core.detector import detect
from unirun.core.search import find_file, fuzzy_find
from unirun.core.history import add_entry, show_history
from unirun.core.install import install_package
from unirun.core.search_command import search_files
from unirun.runtimes import wine, waydroid, appimage, native
from unirun.config import load_config

VERBOSE = False

def log(msg):
    if VERBOSE:
        print(f"[UniRun] {msg}")

def show_help():
    print(f"""
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
    config              Show current configuration.

OPTIONS:
    --verbose, -v       Enable verbose logging.

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
    unirun --verbose setup.exe          -> Run with detailed logging
======================================================================
""")

def show_version():
    print(f"UniRun v{VERSION}")

def run_file(filepath):
    if filepath.startswith("http://") or filepath.startswith("https://"):
        add_entry(filepath)
        print(f"\n[UniRun] Remote web target identified. Routing via Web Engine...")
        xdg.launch(filepath)
        return

    if not os.path.exists(filepath):
        system_binary = shutil.which(filepath)
        if system_binary:
            log(f"Resolved '{filepath}' to system binary: {system_binary}")
            filepath = system_binary
        else:
            print(f"[UniRun] Local target not found. Checking filesystem via fuzzy lookup...")
            found = find_file(filepath)
            if not found:
                found = fuzzy_find(filepath)
            if found:
                print(f"[UniRun] Resolved: Target located at -> {found}")
                filepath = found
            else:
                print(f"[UniRun] Error: Specified file or command path token could not be resolved: '{filepath}'")
                return

    add_entry(filepath)
    runtime = detect(filepath)

    print(f"[UniRun] Binary analysis complete. Target layer: [{runtime.upper()}]")
    log(f"Full path: {os.path.abspath(filepath)}")

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

def show_config():
    cfg = load_config()
    print(f"\nUniRun Configuration ({cfg._path}):")
    print(f"  search_dirs: {cfg.get('search_dirs', ['default'])}")
    print(f"  history_file: {cfg.get('history_file', '~/.local/share/unirun/history.log')}")
    print()

def main():
    global VERBOSE

    # Filter out --verbose before argparse to allow direct launch
    args_list = sys.argv[1:]
    verbose_mode = False
    if "--verbose" in args_list or "-v" in args_list:
        verbose_mode = True
        VERBOSE = True
        args_list = [a for a in args_list if a not in ("--verbose", "-v")]

    if not args_list:
        show_help()
        return

    command = args_list[0]
    known_commands = ["help", "version", "doctor", "history", "search", "install", "run", "config"]

    if verbose_mode and command not in known_commands:
        log(f"Direct launch mode for: {command}")

    if command not in known_commands:
        run_file(command)
        return

    if command == "help":
        show_help()
    elif command == "version":
        show_version()
    elif command == "doctor":
        doctor()
    elif command == "config":
        show_config()
    elif command == "history":
        show_history()
    elif command == "search":
        if len(args_list) < 2:
            print("[UniRun] Error: Missing search parameters. Syntax: unirun search <query>")
            return
        search_files(args_list[1])
    elif command == "install":
        if len(args_list) < 2:
            print("[UniRun] Error: Missing target name. Syntax: unirun install <package>")
            return
        install_package(args_list[1])
    elif command == "run":
        if len(args_list) < 2:
            print("[UniRun] Error: Missing targeted execution reference file path.")
            return
        run_file(args_list[2])
    else:
        print("[UniRun] Error: Unknown command entered.")

if __name__ == "__main__":
    main()
