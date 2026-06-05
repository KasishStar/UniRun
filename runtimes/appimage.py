import os
import subprocess

def launch(filepath):
    print(f"[UniRun] Launching AppImage: {filepath}")

    os.chmod(filepath, 0o755)

    subprocess.run([
        filepath
    ])