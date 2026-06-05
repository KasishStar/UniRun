import subprocess

def launch(filepath):
    print(f"[UniRun] Launching Windows app: {filepath}")

    subprocess.run([
        "wine",
        filepath
    ])