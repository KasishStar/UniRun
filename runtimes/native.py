import os
import subprocess
import sys

def launch(filepath):
    # Check if the path is a directory
    if os.path.isdir(filepath):
        print(f"[UniRun] Target '{filepath}' is a directory.")
        print(f"[UniRun] Handing off to system file explorer/XDG...")
        # Fallback to opening directories with xdg-open safely
        subprocess.Popen(["xdg-open", filepath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return

    # Check if the file is missing execution permissions
    if not os.access(filepath, os.X_OK):
        print(f"[UniRun] Error: File is not executable: {filepath}")
        print(f"[UniRun] Hint: Run 'chmod +x \"{filepath}\"' to allow execution.")
        return

    print(f"[UniRun] Launching native file: {filepath}")
    
    try:
        # Using Popen and decoupling avoids terminal log flooding and locks
        subprocess.Popen(
            [filepath],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setpgrp # Decouples process groups so Ctrl+C on your shell won't kill the launched app
        )
    except Exception as e:
        print(f"[UniRun] Failed to execute target native file: {e}")