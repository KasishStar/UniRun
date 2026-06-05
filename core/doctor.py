import shutil
import os


def check_command(name):
    return shutil.which(name) is not None


def check_proton():

    proton_paths = [
        os.path.expanduser("~/.steam/steam/steamapps/common"),
        os.path.expanduser("~/.local/share/Steam/steamapps/common")
    ]

    for path in proton_paths:

        if os.path.exists(path):

            for item in os.listdir(path):

                if "Proton" in item:
                    return True

    return False


def doctor():

    checks = {
        "Wine": check_command("wine"),
        "Waydroid": check_command("waydroid"),
        "Flatpak": check_command("flatpak"),
        "Steam": check_command("steam"),
        "Java": check_command("java"),
        "Python": check_command("python"),
        "Git": check_command("git"),
        "Proton": check_proton()
    }

    print("\nUniRun Doctor\n")

    for name, status in checks.items():

        icon = "✓" if status else "✗"

        state = "Installed" if status else "Missing"

        print(f"{icon} {name:<10} {state}")

    print()