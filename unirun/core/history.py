import os
import datetime
from unirun.config import load_config

def get_history_file():
    cfg = load_config()
    return os.path.expanduser(cfg.get("history_file", "~/.local/share/unirun/history.log"))

def add_entry(filepath):
    history_file = get_history_file()
    try:
        os.makedirs(os.path.dirname(history_file), exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        absolute_target = os.path.abspath(filepath) if os.path.exists(filepath) else filepath
        with open(history_file, "a") as f:
            f.write(f"[{timestamp}] LAUNCH: {absolute_target}\n")
    except Exception:
        pass

def show_history():
    history_file = get_history_file()
    if not os.path.exists(history_file) or os.path.getsize(history_file) == 0:
        print("[UniRun] History: Execution log register is completely empty.")
        return

    print("\n======================================")
    print("  UniRun Execution Logs")
    print("======================================")
    try:
        with open(history_file) as f:
            records = f.readlines()
            for record in records[-25:]:
                print(record.strip())
    except Exception as e:
        print(f"[UniRun] Error: Failed to access runtime history log: {e}")
    print("======================================\n")
