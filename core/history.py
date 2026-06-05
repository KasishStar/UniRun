from pathlib import Path

HISTORY_FILE = Path.home() / ".unirun_history"


def add_entry(filepath):

    with open(HISTORY_FILE, "a") as f:
        f.write(filepath + "\n")


def show_history():

    if not HISTORY_FILE.exists():
        print("No launch history")
        return

    print("\nRecent UniRun Launches\n")

    lines = HISTORY_FILE.read_text().splitlines()

    for i, entry in enumerate(reversed(lines[-20:]), start=1):
        print(f"{i}. {entry}")