from pathlib import Path

def detect(filepath):
    ext = Path(filepath).suffix.lower()

    if ext in [".exe", ".msi"]:
        return "windows"

    elif ext == ".apk":
        return "android"

    elif ext == ".appimage":
        return "appimage"

    else:
        return "native"