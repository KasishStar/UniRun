import os
import subprocess
import sys
from unirun.config import load_config
from unirun.ui import C, info, ok, warn, dim

def get_prefix_path():
    cfg = load_config()
    return os.path.expanduser(cfg.get("wine_prefix", "~/.local/share/unirun/prefixes/default"))

def ensure_prefix():
    prefix = get_prefix_path()
    if not os.path.exists(os.path.join(prefix, "drive_c")):
        print(f"  {info('Creating Wine prefix...')} ({dim(prefix)})")
        env = os.environ.copy()
        env["WINEPREFIX"] = prefix
        subprocess.run(["wineboot", "-u"], env=env,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"  {ok('Wine prefix ready')}")
    return prefix

def launch(filepath):
    game_dir = os.path.dirname(os.path.abspath(filepath))
    game_exe = os.path.basename(filepath)

    prefix = ensure_prefix()
    env = os.environ.copy()
    env["WINEPREFIX"] = prefix
    env["WINEDLLOVERRIDES"] = "winemenubuilder.exe=d"

    print(f"  {info(f'Wine prefix: {dim(prefix)}')}")
    print(f"  {info(f'Working dir: {dim(game_dir)}')}")
    print(f"  {ok('Launching with Wine...')}")

    try:
        subprocess.Popen(
            ["wine", game_exe],
            cwd=game_dir,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setpgrp
        )
        print(f"  {ok('App launched in background')}")
    except Exception as e:
        print(f"  {warn(f'Failed: {e}')}")
