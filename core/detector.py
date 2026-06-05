from pathlib import Path


DOCUMENTS = {
    ".pdf",
    ".txt",
    ".md"
}

IMAGES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif"
}

VIDEOS = {
    ".mp4",
    ".mkv",
    ".webm",
    ".avi"
}

AUDIO = {
    ".mp3",
    ".wav",
    ".flac",
    ".ogg"
}


def detect(filepath):

    if filepath.startswith("http://"):
        return "web"

    if filepath.startswith("https://"):
        return "web"

    ext = Path(filepath).suffix.lower()

    if ext in [".exe", ".msi"]:
        return "windows"

    elif ext == ".apk":
        return "android"

    elif ext == ".appimage":
        return "appimage"

    elif ext in DOCUMENTS:
        return "xdg"

    elif ext in IMAGES:
        return "xdg"

    elif ext in VIDEOS:
        return "xdg"

    elif ext in AUDIO:
        return "xdg"

    return "native"