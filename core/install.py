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
    "heroic": "heroic-games-launcher",
    "flatpak": "flatpak",
    "java": "jdk-openjdk",
    "proton": "protonup-cli"
}


def install_package(name):
    # Convert incoming input string to lowercase to handle capitalization mistakes
    package = PACKAGES.get(name.lower())

    if not package:
        print(f"[UniRun] Unknown package: {name}")
        return

    print(f"[UniRun] Installing {package} via system package manager...")

    subprocess.run([
        "sudo",
        "pacman",
        "-S",
        package
    ])