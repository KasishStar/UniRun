import subprocess


def launch(filepath):

    print(f"[UniRun] Launching native file: {filepath}")

    subprocess.run([
        filepath
    ])