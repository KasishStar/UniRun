import json
import os
import subprocess
import shutil
from unirun.ui import C, header, bold, dim, info, warn, fail, ok, confirm

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
APPS_FILE = os.path.join(DATA_DIR, "apps.json")

def load_apps():
    if not os.path.exists(APPS_FILE):
        return {}
    with open(APPS_FILE) as f:
        return json.load(f).get("apps", {})

def resolve_app_name(query):
    apps = load_apps()
    query = query.lower().strip()
    if query in apps:
        return query, apps[query]
    for aid, app in apps.items():
        if query == app["name"].lower():
            return aid, app
        if query in aid:
            return aid, app
    return None, None

def install_source(source):
    pkg = source["package"]
    stype = source["type"]

    if stype == "pacman":
        print(f"  {info('Installing via pacman...')}")
        return subprocess.run(["sudo", "pacman", "-S", "--noconfirm", pkg]).returncode == 0
    elif stype == "aur":
        if shutil.which("yay"):
            print(f"  {info('Installing via yay (AUR)...')}")
            return subprocess.run(["yay", "-S", "--noconfirm", pkg]).returncode == 0
        print(f"  {warn('yay not found. Install it first: unirun install yay')}")
        return False
    elif stype == "flatpak":
        if shutil.which("flatpak"):
            print(f"  {info('Installing via flatpak...')}")
            return subprocess.run(["flatpak", "install", "flathub", pkg, "-y"]).returncode == 0
        print(f"  {warn('flatpak not found. Install it first: unirun install flatpak')}")
        return False
    else:
        print(f"  {fail(f'Unknown install type: {stype}')}")
        return False

def install_app(app_id):
    aid, app = resolve_app_name(app_id)
    if not app:
        print(f"  {fail(f'App not found: {app_id}')}")
        print(f"  {dim('Check the name or add it to the database.')}")
        return

    print(header(f"Install: {app['name']}"))
    print(f"  {dim(app['description'])}")
    print(f"  {bold('Categories:')} {', '.join(app['categories'])}")
    print()

    if app.get("paid"):
        url = app.get("url", "")
        print(f"  {warn('This app may require a paid account or license.')}")
        if url:
            print(f"  {bold('Website:')} {C.CYN}{url}{C.RST}")
        if not confirm("Continue with install?", False):
            print(f"  {warn('Cancelled.')}")
            return

    sources = app["sources"]
    if len(sources) == 0:
        print(f"  {fail('No install sources available.')}")
        return

    selected = None
    if len(sources) == 1:
        selected = sources[0]
    else:
        print(f"  {bold('Available sources:')}")
        for i, src in enumerate(sources):
            rec = f" {C.LGRN}(Recommended){C.RST}" if src.get("recommended") else ""
            free_tag = f" {C.GRN}(Free){C.RST}" if src.get("free") else f" {C.YLW}(Paid){C.RST}"
            src_name = src.get("source", src["type"])
            print(f"  {C.CYN}{i+1}.{C.RST} {src_name}{rec}{free_tag}")
            print(f"     {dim(f'{src[\"type\"]}: {src[\"package\"]}')}")
        print()

        raw = input(f"  {bold('Select source')} [1-{len(sources)}]: ").strip()
        try:
            idx = int(raw) - 1
            selected = sources[idx] if 0 <= idx < len(sources) else sources[0]
        except (ValueError, IndexError):
            selected = sources[0]

    if not selected.get("free") and selected.get("url"):
        print(f"  {warn('This source requires payment/subscription.')}")
        print(f"  {C.CYN}{selected['url']}{C.RST}")
        if not confirm("Continue?", False):
            print(f"  {warn('Cancelled.')}")
            return

    print(f"  {ok(f'Selected: {selected[\"source\"]}')}")
    print()

    if install_source(selected):
        print(f"  {ok(f'{app[\"name\"]} installed successfully!')}")
    else:
        print(f"  {fail(f'Failed to install {app[\"name\"]}')}")
