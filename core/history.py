import os
import datetime

HISTORY_FILE = os.path.expanduser("~/.local/share/unirun/history.log")

def add_entry(filepath):
    """Logs an authenticated execution trace record to the local cache storage."""
    try:
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        absolute_target = os.path.abspath(filepath) if os.path.exists(filepath) else filepath
        
        with open(HISTORY_FILE, "a") as f:
            f.write(f"[{timestamp}] LAUNCH: {absolute_target}\n")
    except Exception as e:
        # Silent pass on history trace errors to avoid breaking execution lifecycles
        pass

def show_history():
    """Displays the system execution sequence history in chronological tracking layout."""
    if not os.path.exists(HISTORY_FILE) or os.path.getsize(HISTORY_FILE) == 0:
        print("[UniRun] HISTORY: Execution log register is completely empty.")
        return

    print("\n======================================================================")
    print("  UniRun Central Core System Execution Logs")
    print("======================================================================")
    try:
        with open(HISTORY_FILE, "r") as f:
            records = f.readlines()
            # Show last 25 entries to avoid spamming the console frame
            for record in records[-25:]:
                print(record.strip())
    except Exception as e:
        print(f"[UniRun] ERROR: Failed to access runtime history log: {e}")
    print("======================================================================\n")