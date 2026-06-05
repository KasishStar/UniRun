import subprocess

def launch(filepath):
    print(f"[UniRun] Installing Android app: {filepath}")

    subprocess.run([
        "waydroid",
        "app",
        "install",
        filepath
    ])