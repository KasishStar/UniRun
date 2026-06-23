import os
import subprocess
import sys

def launch(filepath):
    print(f"[UniRun]  Initializing environment prefixes...")

    # Get the absolute folder containing the executable (e.g., GTA San Andreas folder)
    game_dir = os.path.dirname(os.path.abspath(filepath))
    game_exe = os.path.basename(filepath)

    # Setup the isolation layer environment variables
    # (Keeps the default prefix pristine or allows custom overrides seamlessly)
    env = os.environ.copy()
    if "WINEPREFIX" not in env:
        env["WINEPREFIX"] = os.path.expanduser("~/.local/share/unirun/prefixes/default")
    
    # Ensure the custom prefix directory layout exists
    os.makedirs(env["WINEPREFIX"], exist_ok=True)

    print(f"[UniRun]  Working Directory Context shifted to: {game_dir}")
    print(f"[UniRun]  Handing off process sequence to Wine environment...")

    try:
        # 1. cwd=game_dir changes the terminal context to the game's folder right before launch
        # 2. Popen with DEVNULL keeps your terminal beautiful and free of Wine clutter logs
        # 3. preexec_fn=os.setpgrp prevents terminal signals from crashing the app process
        subprocess.Popen(
            ["wine", game_exe],
            cwd=game_dir,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setpgrp
        )
        print(f"[UniRun]  App launched successfully in detached state.")
    except Exception as e:
        print(f"[UniRun] ❌ Critical: Failed to launch Wine backend instance: {e}")