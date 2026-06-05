import subprocess


PACKAGES = {
    "wine": "wine",
    "steam": "steam",
    "waydroid": "waydroid",
    "git": "git",
    "python": "python",
    "lutris": "lutris",
    "bottles": "bottles",
    "protonup-qt": "protonup-qt",
    "heroic": "heroic-games-launcher"
}


def install_package(name):

    package = PACKAGES.get(name)

    if not package:
        print(f"[UniRun] Unknown package: {name}")
        return

    print(f"[UniRun] Installing {package}")

    subprocess.run([
        "sudo",
        "pacman",
        "-S",
        package
    ])