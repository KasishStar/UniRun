import sys
import os
import shutil
import textwrap

from unirun import VERSION
from unirun.runtimes import xdg
from unirun.core.doctor import doctor as run_doctor
from unirun.core.detector import detect, get_file_info
from unirun.core.search import find_file, fuzzy_find
from unirun.core.history import add_entry, show_history
from unirun.core.install import install_app, load_apps, resolve_app_name
from unirun.core.search_command import search_files
from unirun.runtimes import wine, waydroid, appimage, native
from unirun.config import load_config, reset_config
from unirun.ui import C, ok, fail, warn, info, bold, dim, header, runtime_badge, confirm, format_size

VERBOSE = False

def log(msg):
    if VERBOSE:
        print(f"  {C.DIM}{msg}{C.RST}")

def show_banner():
    w = shutil.get_terminal_size().columns
    print(f"""
  {C.BLD}{C.CYN}U n i R u n{C.RST}  {C.DIM}v{VERSION}{C.RST}
  {C.DIM}{'─' * min(w - 2, 40)}{C.RST}
  {dim('Run Anything. Anywhere.')}
""")

def show_help():
    show_banner()
    print(f"""  {bold('USAGE')}
    {C.GRN}unirun{C.RST} {dim('<command>')} {dim('[args]')}
    {C.GRN}unirun{C.RST} {dim('<file>')}        {dim('# auto-detect and run')}

  {bold('COMMANDS')}
    {C.GRN}run{C.RST}     {dim('<file>')}     Run a file with auto-detected runtime
    {C.GRN}info{C.RST}    {dim('<file>')}     Show file type and suggested runtime
    {C.GRN}search{C.RST}  {dim('<query>')}   Search filesystem for matching files
    {C.GRN}install{C.RST} {dim('<pkg>')}     Install a runtime or package
    {C.GRN}doctor{C.RST}              Check installed runtimes status
    {C.GRN}setup{C.RST}              Interactive configuration wizard
    {C.GRN}history{C.RST}             Show recently launched files
    {C.GRN}config{C.RST}              Show current configuration
    {C.GRN}version{C.RST}             Show version
    {C.GRN}help{C.RST}                Show this help

  {bold('OPTIONS')}
    {C.GRN}-v{C.RST}, {C.GRN}--verbose{C.RST}  Enable detailed logging

  {bold('EXAMPLES')}
    {dim('unirun setup.exe')}       {dim('# Auto-runs via Wine')}
    {dim('unirun game.apk')}        {dim('# Installs via Waydroid')}
    {dim('unirun firefox')}         {dim('# Launches system binary')}
    {dim('unirun info file.exe')}   {dim('# Shows file details')}
    {dim('unirun -v setup.exe')}    {dim('# Run with debug logs')}
""")

def show_version():
    print(f"  UniRun v{VERSION}")

def show_config():
    cfg = load_config()
    print(header("Configuration"))
    print(f"  {bold('Config file:')} {cfg._path}")
    print(f"  {bold('Search dirs:')} {len(cfg.get('search_dirs', []))} directories")
    print(f"  {bold('History:')}    {cfg.get('history_file')}")
    print()

def run_file(filepath):
    is_url = filepath.startswith("http://") or filepath.startswith("https://")

    if not is_url and not os.path.exists(filepath):
        system_binary = shutil.which(filepath)
        if system_binary:
            log(f"Resolved '{filepath}' to: {system_binary}")
            filepath = system_binary
        else:
            print(f"  {warn('File not found, searching...')}")
            found = find_file(filepath)
            if not found:
                found = fuzzy_find(filepath)
            if found:
                print(f"  {ok('Found at:')} {found}")
                filepath = found
            else:
                print(f"  {fail(f'Could not resolve: {filepath}')}")
                # Check if it's in the app database
                aid, app = resolve_app_name(filepath)
                if app:
                    app_name = app["name"]
                    print(f"  {info(f'{app_name} is not installed.')}")
                    if confirm(f"Install {app['name']}?", True):
                        install_app(aid)
                    else:
                        print(f"  {dim('Run: unirun install ' + aid + ' to install later')}")
                return

    if is_url:
        runtime = "web"
    else:
        info_data = get_file_info(filepath)
        runtime = info_data["runtime"]
        print(f"  {ok('Detected:')} {info_data['type_name']}  {runtime_badge(runtime)}")
        size_str = info_data["size"]
        if size_str:
            print(f"  {dim(f'Size: {size_str}')}")
        if not is_url and runtime in ("native", "windows") and info_data["ext"] not in (".exe", ".msi"):
            if not confirm(f"Run '{os.path.basename(filepath)}' as {runtime.upper()}?", True):
                print(f"  {warn('Cancelled')}")
                return

    add_entry(filepath)
    log(f"Runtime: {runtime}")

    runners = {
        "windows": wine.launch,
        "android": waydroid.launch,
        "appimage": appimage.launch,
        "xdg": xdg.launch,
        "web": xdg.launch,
        "native": native.launch,
    }
    runner = runners.get(runtime, native.launch)
    try:
        runner(filepath)
    except Exception as e:
        print(f"  {fail(f'Failed: {e}')}")

def cmd_info(filepath):
    if not os.path.exists(filepath):
        print(f"  {fail('File not found')}")
        return

    info_data = get_file_info(filepath)
    name = os.path.basename(filepath)

    print(header(f"File: {name}"))
    print(f"  {bold('Path:')}    {os.path.abspath(filepath)}")
    print(f"  {bold('Size:')}    {info_data['size']}")
    print(f"  {bold('Type:')}    {info_data['type_name']}")
    print(f"  {bold('Ext:')}     {info_data['ext'] or '(none)'}")
    print(f"  {bold('Runtime:')} {runtime_badge(info_data['runtime'])}")
    if info_data["executable"] is not None:
        print(f"  {bold('Exec:')}    {'Yes' if info_data['executable'] else 'No'}")
    print()

def cmd_setup():
    print(header("UniRun Setup"))
    print(f"  This will create a config file at ~/.config/unirun/config.json\n")

    cfg = load_config()
    dirs = cfg.get("search_dirs", [])

    print(f"  {bold('Search directories')} (where UniRun looks for files):")
    new_dirs = []
    for d in ["~/Downloads", "~/Documents", "~/Desktop", "~/Pictures", "~/Videos", "~/Music"]:
        expanded = os.path.expanduser(d)
        exists = "✓" if os.path.isdir(expanded) else " "
        if confirm(f"  Search [{exists}] {d}?", d in dirs or os.path.isdir(expanded)):
            new_dirs.append(d)

    cfg.set("search_dirs", new_dirs)
    print(f"\n  {ok('Configuration saved!')}")
    print(f"  {dim('Edit manually: ~/.config/unirun/config.json')}\n")

def cmd_doctor():
    run_doctor()

def cmd_search(query):
    results = search_files(query, raw=True)
    if not results:
        print(f"  {warn(f'No results for: {query}')}")
        return
    print(header(f"Search: {query}"))
    for i, r in enumerate(results[:20], 1):
        print(f"  {C.DIM}{i:>3}.{C.RST} {r}")
    if len(results) > 20:
        print(f"  {dim(f'... and {len(results) - 20} more')}")
    print()

def main():
    global VERBOSE

    args = [a for a in sys.argv[1:] if a not in ("--verbose", "-v")]
    if len(sys.argv) != len(args) + 1:
        VERBOSE = True

    if not args:
        show_help()
        return

    cmd = args[0]
    cmds = ["help", "version", "doctor", "history", "search", "install", "run", "config", "setup", "info"]

    if cmd not in cmds:
        if VERBOSE:
            log(f"Direct launch: {cmd}")
        run_file(cmd)
        return

    if cmd == "help":
        show_help()
    elif cmd == "version":
        show_version()
    elif cmd == "doctor":
        cmd_doctor()
    elif cmd == "config":
        show_config()
    elif cmd == "setup":
        cmd_setup()
    elif cmd == "history":
        show_history()
    elif cmd == "info":
        if len(args) < 2:
            print(f"  {fail('Usage: unirun info <file>')}")
            return
        cmd_info(args[1])
    elif cmd == "search":
        if len(args) < 2:
            print(f"  {fail('Usage: unirun search <query>')}")
            return
        cmd_search(args[1])
    elif cmd == "install":
        if len(args) < 2:
            print(f"  {fail('Usage: unirun install <app_id>')}")
            return
        install_app(args[1])
    elif cmd == "run":
        if len(args) < 2:
            print(f"  {fail('Usage: unirun run <file>')}")
            return
        run_file(args[1])
    else:
        print(f"  {fail('Unknown command. Try: unirun help')}")

if __name__ == "__main__":
    main()
