import subprocess
import shutil


def launch(filepath):

    if shutil.which("waydroid") is None:
        print("[UniRun] Waydroid is not installed")
        return

    print(f"[UniRun] Installing Android app: {filepath}")

    subprocess.run([
        "waydroid",
        "app",
        "install",
        filepath
    ])