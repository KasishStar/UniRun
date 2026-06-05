import subprocess


def launch(filepath):
    print(f"[UniRun] Opening with xdg-open: {filepath}")

    subprocess.run([
        "xdg-open",
        filepath
    ])