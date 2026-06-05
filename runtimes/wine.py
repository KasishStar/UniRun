import subprocess
import shutil


def launch(filepath):

    if shutil.which("wine") is None:
        print("[UniRun] Wine is not installed")
        print("Install with:")
        print("sudo pacman -S wine")
        return

    print(f"[UniRun] Launching Windows app: {filepath}")

    subprocess.run([
        "wine",
        filepath
    ])