import shutil
import os
from unirun.ui import C, ok, fail, warn, info, bold, dim, header, subheader

RUNTIME_CHECKS = [
    ("Wine", "wine", "windows", "Run Windows (.exe, .msi) applications"),
    ("Waydroid", "waydroid", "android", "Run Android (.apk) applications"),
    ("Flatpak", "flatpak", "xdg", "Run sandboxed Flatpak applications"),
    ("Steam", "steam", "native", "Run Steam games (Proton for Windows games)"),
    ("Java", "java", "native", "Run Java applications (.jar)"),
    ("Python", "python3", "native", "Run Python scripts"),
    ("Git", "git", None, "Version control (needed for AUR installs)"),
]

SUGGESTIONS = {
    "wine": "  Install: sudo pacman -S wine",
    "waydroid": "  Install: yay -S waydroid\n  Then: sudo waydroid init",
    "flatpak": "  Install: sudo pacman -S flatpak\n  Then: flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo",
    "steam": "  Install: sudo pacman -S steam",
    "java": "  Install: sudo pacman -S jdk-openjdk",
    "python3": "",
    "git": "  Install: sudo pacman -S git",
}

def check_command(name):
    return shutil.which(name) is not None

def check_proton():
    proton_paths = [
        os.path.expanduser("~/.steam/steam/steamapps/common"),
        os.path.expanduser("~/.local/share/Steam/steamapps/common"),
    ]
    for path in proton_paths:
        if os.path.exists(path):
            for item in os.listdir(path):
                if "Proton" in item:
                    return True
    return False

def doctor():
    print(header("UniRun Doctor"))
    print(f"  {dim('Checking system runtimes...')}\n")

    all_ok = True
    for name, cmd, runtime, desc in RUNTIME_CHECKS:
        installed = check_command(cmd)
        if not installed:
            all_ok = False

        status = ok("Ready") if installed else fail("Missing")
        runtime_tag = f" {C.DIM}[{runtime}]{C.RST}" if runtime else ""
        print(f"  {bold(name):<12} {status}{runtime_tag}")

    # Proton check separately
    proton = check_proton()
    if not proton:
        all_ok = False
    pstatus = ok("Ready") if proton else fail("Missing")
    print(f"  {bold('Proton'):<12} {pstatus} {C.DIM}[windows]{C.RST}")

    print()
    if not all_ok:
        print(f"  {warn('Some runtimes are missing — suggested fixes:')}\n")
        for name, cmd, runtime, desc in RUNTIME_CHECKS:
            if not check_command(cmd) and SUGGESTIONS.get(cmd):
                print(f"  {bold(name)} ({desc})")
                print(f"  {SUGGESTIONS[cmd]}")
                print()
        if not proton:
            print(f"  {bold('Proton')} (Play Windows games via Steam)")
        print(f"  {info('Run: unirun install <package> to auto-install')}")
    else:
        print(f"  {ok('All runtimes are ready!')}")

    print()
